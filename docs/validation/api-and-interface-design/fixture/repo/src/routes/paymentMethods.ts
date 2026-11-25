import { Router } from 'express';
import { db } from '../db';

export const paymentMethods = Router();

// Replaces the whole payment method. The dashboard always sends every field.
paymentMethods.put('/api/payment-methods/:id', async (req, res) => {
  const { label, cardToken, isDefault } = req.body;
  if (!label || !cardToken) {
    return res.status(400).json({ message: 'label and cardToken required' });
  }
  const row = await db.query(
    'UPDATE payment_methods SET label = $1, card_token = $2, is_default = $3 WHERE id = $4 RETURNING *',
    [label, cardToken, isDefault ?? false, req.params.id],
  );
  if (row.rowCount === 0) return res.status(404).send('not found');
  return res.json(row.rows[0]);
});
