/**
 * Type definitions for the chat interface
 */

export interface ChatMessage {
  id: string;
  userId?: string;
  message: string;
  sender: 'user' | 'system';
  timestamp: Date;
  intent?: string;
  actionTaken?: any;
}

export interface ChatResponse {
  response: string;
  intent: string;
  actionTaken?: any;
}

export interface ChatRequest {
  message: string;
}

export interface IntentClassification {
  name: string;
  description: string;
  confidence: number;
}

export interface ChatHistory {
  sessionId?: string;
  messages: ChatMessage[];
}