// src/mail/SesMailer.ts
import { SESClient, SendEmailCommand } from "@aws-sdk/client-ses";
import { IMailer } from "./IMailer";

const FROM = "billing@example.com";

export class SesMailer implements IMailer {
  private readonly ses = new SESClient({ region: process.env.AWS_REGION ?? "eu-west-1" });

  async send(to: string, subject: string, body: string): Promise<void> {
    await this.ses.send(
      new SendEmailCommand({
        Source: FROM,
        Destination: { ToAddresses: [to] },
        Message: { Subject: { Data: subject }, Body: { Text: { Data: body } } },
      }),
    );
  }
}
