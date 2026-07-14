export interface Settlement {
  from_user: string;
  from_user_id: string;

  to_user: string;
  to_user_id: string;

  amount: number;
}