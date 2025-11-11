import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document, Types } from 'mongoose';

export type QuizResultDocument = QuizResult & Document;

@Schema({ timestamps: true })
export class QuizResult {
  @Prop({ type: Types.ObjectId, ref: 'User', required: true })
  userId: Types.ObjectId;

  @Prop({ required: true })
  score: number;

  @Prop({ required: true })
  totalQuestions: number;

  @Prop({ required: true })
  correctAnswers: number;

  @Prop({ required: true })
  incorrectAnswers: number;

  @Prop({ type: [Object], default: [] })
  answers: Array<{
    question: string;
    userAnswer: string;
    correctAnswer: string;
    isCorrect: boolean;
  }>;

  @Prop({ required: true })
  completedAt: Date;
}

export const QuizResultSchema = SchemaFactory.createForClass(QuizResult);
