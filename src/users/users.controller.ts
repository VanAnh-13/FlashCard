import { Controller, Get, Put, Body, UseGuards, Request } from '@nestjs/common';
import { UsersService } from './users.service';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';

@Controller('users')
@UseGuards(JwtAuthGuard)
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get('profile')
  async getProfile(@Request() req) {
    return this.usersService.findOne(req.user.userId);
  }

  @Put('profile')
  async updateProfile(@Request() req, @Body() updateData: any) {
    return this.usersService.update(req.user.userId, updateData);
  }

  @Get('stats')
  async getStats(@Request() req) {
    const user = await this.usersService.findOne(req.user.userId);
    return {
      wordsLearned: user.wordsLearned,
      studyStreak: user.studyStreak,
      dailyGoal: user.dailyGoal,
      achievements: user.achievements,
    };
  }
}
