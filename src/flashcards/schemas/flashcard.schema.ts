import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';

export type FlashcardDocument = Flashcard & Document;

@Schema({ timestamps: true })
export class Flashcard {
  @Prop({ required: true })
  korean: string;

  @Prop({ required: true })
  english: string;

  @Prop({ required: true })
  exampleKorean: string;

  @Prop({ required: true })
  exampleEnglish: string;

  @Prop({ default: 'basic' })
  category: string;

  @Prop({ default: 1 })
  difficulty: number;
}

export const FlashcardSchema = SchemaFactory.createForClass(Flashcard);
