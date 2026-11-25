import { send } from '../src/notifications/sender';
import { pickChannel } from '../src/notifications/channels';
import { withRetry } from '../src/notifications/retry';

jest.mock('../src/notifications/sender');

test('sms users get sms', async () => {
  const channel = pickChannel({ sms: true });
  await withRetry(3, () => send(channel, { phone: '+100' }, 'hi'));
  expect(send).toHaveBeenCalledWith('sms', { phone: '+100' }, 'hi');
});
