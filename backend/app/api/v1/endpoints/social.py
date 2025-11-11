"""
Social Features Endpoints - Friends, Groups, Activity Feed
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta
from bson import ObjectId
from typing import List

from app.models.social import (
    FriendRequest,
    Friend,
    StudyGroup,
    GroupMember,
    Post,
    ActivityFeed
)
from app.api.dependencies import get_current_user
from app.core.database import get_database

router = APIRouter()


# ===== Friends Management =====

@router.get("/friends", response_model=List[Friend])
async def get_friends(current_user: dict = Depends(get_current_user)):
    """Get user's friends list"""
    db = get_database()
    users_collection = db.users

    friend_ids = current_user.get("friends", [])

    if not friend_ids:
        return []

    # Get friends' details
    friends = await users_collection.find({
        "_id": {"$in": [ObjectId(fid) if isinstance(fid, str) else fid for fid in friend_ids]}
    }).to_list(length=1000)

    return [
        Friend(
            user_id=str(f["_id"]),
            username=f["username"],
            profile_picture=f.get("profile_picture", ""),
            level=f.get("level", "Beginner"),
            total_points=f.get("total_points", 0),
            words_learned=f.get("words_learned", 0),
            study_streak=f.get("study_streak", 0),
            is_online=f.get("is_online", False)
        )
        for f in friends
    ]


@router.post("/friends/request/{user_id}")
async def send_friend_request(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Send a friend request"""
    db = get_database()
    friend_requests_collection = db.friend_requests
    users_collection = db.users

    # Check if user exists
    target_user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if already friends
    if user_id in current_user.get("friends", []):
        raise HTTPException(status_code=400, detail="Already friends")

    # Check if request already exists
    existing_request = await friend_requests_collection.find_one({
        "$or": [
            {"from_user_id": current_user["_id"], "to_user_id": ObjectId(user_id), "status": "pending"},
            {"from_user_id": ObjectId(user_id), "to_user_id": current_user["_id"], "status": "pending"}
        ]
    })

    if existing_request:
        raise HTTPException(status_code=400, detail="Friend request already exists")

    # Create friend request
    request_doc = {
        "from_user_id": current_user["_id"],
        "to_user_id": ObjectId(user_id),
        "status": "pending",
        "created_at": datetime.utcnow()
    }

    await friend_requests_collection.insert_one(request_doc)

    return {"message": "Friend request sent"}


@router.get("/friends/requests/incoming", response_model=List[FriendRequest])
async def get_incoming_requests(current_user: dict = Depends(get_current_user)):
    """Get incoming friend requests"""
    db = get_database()
    friend_requests_collection = db.friend_requests

    cursor = friend_requests_collection.find({
        "to_user_id": current_user["_id"],
        "status": "pending"
    }).sort("created_at", -1)

    requests = await cursor.to_list(length=100)

    return [
        FriendRequest(
            _id=str(r["_id"]),
            from_user_id=str(r["from_user_id"]),
            to_user_id=str(r["to_user_id"]),
            status=r["status"],
            created_at=r["created_at"],
            responded_at=r.get("responded_at")
        )
        for r in requests
    ]


@router.post("/friends/requests/{request_id}/accept")
async def accept_friend_request(
    request_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Accept a friend request"""
    db = get_database()
    friend_requests_collection = db.friend_requests
    users_collection = db.users

    # Get request
    request = await friend_requests_collection.find_one({"_id": ObjectId(request_id)})
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    if request["to_user_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    if request["status"] != "pending":
        raise HTTPException(status_code=400, detail="Request already processed")

    # Update request status
    await friend_requests_collection.update_one(
        {"_id": ObjectId(request_id)},
        {
            "$set": {
                "status": "accepted",
                "responded_at": datetime.utcnow()
            }
        }
    )

    # Add to both users' friends lists
    from_user_id = request["from_user_id"]

    await users_collection.update_one(
        {"_id": current_user["_id"]},
        {"$addToSet": {"friends": str(from_user_id)}}
    )

    await users_collection.update_one(
        {"_id": from_user_id},
        {"$addToSet": {"friends": str(current_user["_id"])}}
    )

    return {"message": "Friend request accepted"}


@router.post("/friends/requests/{request_id}/reject")
async def reject_friend_request(
    request_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Reject a friend request"""
    db = get_database()
    friend_requests_collection = db.friend_requests

    # Get request
    request = await friend_requests_collection.find_one({"_id": ObjectId(request_id)})
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    if request["to_user_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Update request status
    await friend_requests_collection.update_one(
        {"_id": ObjectId(request_id)},
        {
            "$set": {
                "status": "rejected",
                "responded_at": datetime.utcnow()
            }
        }
    )

    return {"message": "Friend request rejected"}


@router.delete("/friends/{friend_id}")
async def remove_friend(
    friend_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Remove a friend"""
    db = get_database()
    users_collection = db.users

    # Remove from both users' friends lists
    await users_collection.update_one(
        {"_id": current_user["_id"]},
        {"$pull": {"friends": friend_id}}
    )

    await users_collection.update_one(
        {"_id": ObjectId(friend_id)},
        {"$pull": {"friends": str(current_user["_id"])}}
    )

    return {"message": "Friend removed"}


@router.get("/users/search")
async def search_users(
    query: str = Query(..., min_length=2),
    limit: int = Query(20, le=50),
    current_user: dict = Depends(get_current_user)
):
    """Search for users by username"""
    db = get_database()
    users_collection = db.users

    # Search by username (case-insensitive)
    cursor = users_collection.find({
        "username": {"$regex": query, "$options": "i"},
        "_id": {"$ne": current_user["_id"]}
    }).limit(limit)

    users = await cursor.to_list(length=limit)

    return [
        {
            "user_id": str(u["_id"]),
            "username": u["username"],
            "profile_picture": u.get("profile_picture", ""),
            "level": u.get("level", "Beginner"),
            "total_points": u.get("total_points", 0),
            "is_friend": str(u["_id"]) in current_user.get("friends", [])
        }
        for u in users
    ]


# ===== Activity Feed =====

@router.get("/feed", response_model=List[ActivityFeed])
async def get_activity_feed(
    limit: int = Query(50, le=100),
    current_user: dict = Depends(get_current_user)
):
    """Get activity feed from friends"""
    db = get_database()
    posts_collection = db.posts
    users_collection = db.users

    # Get friend IDs
    friend_ids = current_user.get("friends", [])
    friend_ids.append(str(current_user["_id"]))  # Include own activities

    # Convert to ObjectId
    friend_oids = [ObjectId(fid) if isinstance(fid, str) else fid for fid in friend_ids]

    # Get recent posts from friends
    cursor = posts_collection.find({
        "user_id": {"$in": friend_oids}
    }).sort("created_at", -1).limit(limit)

    posts = await cursor.to_list(length=limit)

    # Get user details
    user_ids = list(set(p["user_id"] for p in posts))
    users = await users_collection.find({
        "_id": {"$in": user_ids}
    }).to_list(length=len(user_ids))

    user_map = {str(u["_id"]): u for u in users}

    # Build activity feed
    feed = []
    for post in posts:
        user = user_map.get(str(post["user_id"]))
        if user:
            feed.append(ActivityFeed(
                id=str(post["_id"]),
                user_id=str(post["user_id"]),
                username=user["username"],
                profile_picture=user.get("profile_picture", ""),
                activity_type=post.get("post_type", "general"),
                description=post.get("content", ""),
                metadata=post.get("metadata", {}),
                timestamp=post["created_at"]
            ))

    return feed


@router.post("/feed/post")
async def create_post(
    content: str,
    post_type: str = "general",
    metadata: dict = {},
    current_user: dict = Depends(get_current_user)
):
    """Create a new post/activity"""
    db = get_database()
    posts_collection = db.posts

    post_doc = {
        "user_id": current_user["_id"],
        "username": current_user["username"],
        "content": content,
        "post_type": post_type,
        "metadata": metadata,
        "likes": [],
        "comments": [],
        "created_at": datetime.utcnow()
    }

    result = await posts_collection.insert_one(post_doc)

    return {
        "message": "Post created",
        "post_id": str(result.inserted_id)
    }


@router.post("/feed/post/{post_id}/like")
async def like_post(
    post_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Like a post"""
    db = get_database()
    posts_collection = db.posts

    # Add user to likes
    result = await posts_collection.update_one(
        {"_id": ObjectId(post_id)},
        {"$addToSet": {"likes": str(current_user["_id"])}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"message": "Post liked"}


@router.post("/feed/post/{post_id}/comment")
async def comment_on_post(
    post_id: str,
    comment: str,
    current_user: dict = Depends(get_current_user)
):
    """Comment on a post"""
    db = get_database()
    posts_collection = db.posts

    comment_doc = {
        "user_id": str(current_user["_id"]),
        "username": current_user["username"],
        "content": comment,
        "created_at": datetime.utcnow()
    }

    result = await posts_collection.update_one(
        {"_id": ObjectId(post_id)},
        {"$push": {"comments": comment_doc}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"message": "Comment added"}


# ===== Study Groups =====

@router.get("/groups", response_model=List[StudyGroup])
async def get_study_groups(
    current_user: dict = Depends(get_current_user)
):
    """Get user's study groups"""
    db = get_database()
    groups_collection = db.study_groups

    cursor = groups_collection.find({
        "members": str(current_user["_id"])
    })

    groups = await cursor.to_list(length=100)

    return [
        StudyGroup(
            _id=str(g["_id"]),
            name=g["name"],
            description=g["description"],
            created_by=str(g["created_by"]),
            members=g.get("members", []),
            max_members=g.get("max_members", 50),
            is_private=g.get("is_private", False),
            created_at=g["created_at"]
        )
        for g in groups
    ]


@router.post("/groups", response_model=StudyGroup)
async def create_study_group(
    name: str,
    description: str,
    is_private: bool = False,
    max_members: int = 50,
    current_user: dict = Depends(get_current_user)
):
    """Create a new study group"""
    db = get_database()
    groups_collection = db.study_groups

    group_doc = {
        "name": name,
        "description": description,
        "created_by": current_user["_id"],
        "members": [str(current_user["_id"])],
        "max_members": max_members,
        "is_private": is_private,
        "created_at": datetime.utcnow()
    }

    result = await groups_collection.insert_one(group_doc)
    group_doc["_id"] = result.inserted_id

    return StudyGroup(
        _id=str(group_doc["_id"]),
        name=group_doc["name"],
        description=group_doc["description"],
        created_by=str(group_doc["created_by"]),
        members=group_doc["members"],
        max_members=group_doc["max_members"],
        is_private=group_doc["is_private"],
        created_at=group_doc["created_at"]
    )


@router.post("/groups/{group_id}/join")
async def join_study_group(
    group_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Join a study group"""
    db = get_database()
    groups_collection = db.study_groups

    group = await groups_collection.find_one({"_id": ObjectId(group_id)})
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    if len(group.get("members", [])) >= group.get("max_members", 50):
        raise HTTPException(status_code=400, detail="Group is full")

    result = await groups_collection.update_one(
        {"_id": ObjectId(group_id)},
        {"$addToSet": {"members": str(current_user["_id"])}}
    )

    return {"message": "Joined group successfully"}


@router.post("/groups/{group_id}/leave")
async def leave_study_group(
    group_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Leave a study group"""
    db = get_database()
    groups_collection = db.study_groups

    result = await groups_collection.update_one(
        {"_id": ObjectId(group_id)},
        {"$pull": {"members": str(current_user["_id"])}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Group not found")

    return {"message": "Left group successfully"}
