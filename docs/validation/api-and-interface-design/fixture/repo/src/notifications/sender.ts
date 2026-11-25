import { TwilioClient } from '../vendor/twilio';
import { SesClient } from '../vendor/ses';
import { FcmClient } from '../vendor/fcm';
import type { Channel } from './channels';

export async function send(channel: Channel, user: any, body: string): Promise<void> {
  if (channel === 'sms') {
    await new TwilioClient(process.env.TWILIO_KEY!).messages.create({ to: user.phone, body });
  } else if (channel === 'email') {
    await new SesClient(process.env.SES_KEY!).send({ to: user.email, subject: 'Payment update', body });
  } else {
    await new FcmClient(process.env.FCM_KEY!).push({ token: user.push_token, body });
  }
}
