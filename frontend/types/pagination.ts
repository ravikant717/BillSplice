export interface PaginatedResponse<T> {
  items: T[];
  page: number;
  page_size: number;
  total: number;
  pages: number;
}