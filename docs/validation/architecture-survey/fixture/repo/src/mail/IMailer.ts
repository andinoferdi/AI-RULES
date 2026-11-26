// src/mail/IMailer.ts
export interface IMailer {
  send(to: string, subject: string, body: string): Promise<void>;
}
