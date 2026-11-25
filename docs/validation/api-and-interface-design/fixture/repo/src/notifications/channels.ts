export type Channel = 'sms' | 'email' | 'push';

export function pickChannel(prefs: { sms?: boolean; email?: boolean; push?: boolean }): Channel {
  if (prefs.push) return 'push';
  if (prefs.sms) return 'sms';
  return 'email';
}
