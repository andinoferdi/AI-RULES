import { Badge } from './Badge';

type Props = {
  isPending?: boolean;
  isPaid?: boolean;
  isFailed?: boolean;
  isRefunded?: boolean;
  isPartiallyRefunded?: boolean;
  failureReason?: string;
  refundedAmountCents?: number;
  paidAt?: string;
};

// Known bugs: some callers pass isPaid and isRefunded together; others pass
// isPartiallyRefunded without refundedAmountCents and the badge shows "Refunded undefined".
export function PaymentStatusBadge(p: Props) {
  if (p.isFailed) return <Badge tone="red">Failed{p.failureReason ? `: ${p.failureReason}` : ''}</Badge>;
  if (p.isRefunded) return <Badge tone="grey">Refunded</Badge>;
  if (p.isPartiallyRefunded) return <Badge tone="amber">Refunded {p.refundedAmountCents}</Badge>;
  if (p.isPaid) return <Badge tone="green">Paid</Badge>;
  return <Badge tone="blue">Pending</Badge>;
}
