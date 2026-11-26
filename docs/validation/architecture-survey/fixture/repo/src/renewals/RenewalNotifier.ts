// src/renewals/RenewalNotifier.ts
import { IMailer } from "../mail/IMailer";
import { Money, format } from "../money/money";

export class RenewalNotifier {
  constructor(private readonly mailer: IMailer) {}

  sendRenewalEmail(email: string, invoiceId: string, amount: Money): Promise<void> {
    return this.mailer.send(
      email,
      "Your subscription renewed",
      `Invoice ${invoiceId}: ${format(amount)}. Thank you!`,
    );
  }
}
