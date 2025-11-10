import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { MongooseModule } from '@nestjs/mongoose';
import { ServeStaticModule } from '@nestjs/serve-static';
import { join } from 'path';

import { AuthModule } from './auth/auth.module';
import { UsersModule } from './users/users.module';
import { FlashcardsModule } from './flashcards/flashcards.module';
import { QuizModule } from './quiz/quiz.module';
import { ProgressModule } from './progress/progress.module';

@Module({
  imports: [
    // Configuration
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: '.env',
    }),

    // Database
    MongooseModule.forRootAsync({
      imports: [ConfigModule],
      useFactory: async (configService: ConfigService) => ({
        uri: configService.get<string>('MONGODB_URI'),
      }),
      inject: [ConfigService],
    }),

    // Serve static files (HTML, CSS, JS)
    ServeStaticModule.forRoot({
      rootPath: join(__dirname, '..', '..'),
      exclude: ['/api*'],
      serveRoot: '/',
    }),

    // Feature modules
    AuthModule,
    UsersModule,
    FlashcardsModule,
    QuizModule,
    ProgressModule,
  ],
})
export class AppModule {}
