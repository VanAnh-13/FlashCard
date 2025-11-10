import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document, Types } from 'mongoose';

export type UserProgressDocument = UserProgress & Document;

@Schema({ timestamps: true })
export class UserProgress {
  @Prop({ type: Types.ObjectId, ref: 'User', required: true })
  userId: Types.ObjectId;

  @Prop({ type: Types.ObjectId, ref: 'Flashcard', required: true })
  flashcardId: Types.ObjectId;

  @Prop({ default: false })
  known: boolean;

  @Prop({ default: false })
  reviewLater: boolean;

  @Prop({ default: 0 })
  timesReviewed: number;

  @Prop()
  lastReviewedAt: Date;

  @Prop({ default: 0 })
  accuracy: number;
}

export const UserProgressSchema = SchemaFactory.createForClass(UserProgress);
