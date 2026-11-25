export type TemplateName = 'receipt' | 'paid' | 'refund' | 'dunning';

export function renderTemplate(name: TemplateName, vars: Record<string, unknown>): string {
  switch (name) {
    case 'receipt':
      return `Thanks! We received ${vars.amount_cents} ${vars.currency}.`;
    case 'paid':
      return `Your payment of ${vars.amount_cents} went through.`;
    case 'refund':
      return `We refunded ${vars.amount_cents}.`;
    case 'dunning':
      return `Your payment failed. Please update your card.`;
  }
}
