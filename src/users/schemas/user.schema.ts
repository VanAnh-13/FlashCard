import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';

export type UserDocument = User & Document;

@Schema({ timestamps: true })
export class User {
  @Prop({ required: true, unique: true })
  username: string;

  @Prop({ required: true, unique: true })
  email: string;

  @Prop({ required: true })
  password: string;

  @Prop({ default: 'https://lh3.googleusercontent.com/aida-public/AB6AXuC21O5nSDggWM09pPyighOBnT7NHBBfvBB3xi1rzOpkYL3l8VCnbmSHw2oHXf_p1gnbkiFaSywaf6TXAitjIhEtqBd02pI3GynWdxza0SLTMt_sldqLkCNuuNchLXYG72Eddp2yYe_DdS612t_RcY_jtO8_WnyoBNeY9_xW1DQBhDDOaXMSpzDphirEh9TgKYd-ZC6GO7u3yImUlPah_HRtSIp5rS6CpUknNZYSmRQgqpvbPV7kt31uEdgHLYKza9727CNJ0skKqlM' })
  profilePicture: string;

  @Prop({ default: 'Beginner' })
  level: string;

  @Prop({ default: 20 })
  dailyGoal: number;

  @Prop({ default: 0 })
  wordsLearned: number;

  @Prop({ default: 0 })
  studyStreak: number;

  @Prop({ default: [] })
  achievements: string[];

  @Prop({ type: Object, default: {} })
  progress: Record<string, any>;
}

export const UserSchema = SchemaFactory.createForClass(User);
