export interface ApiResponse<T> {
  data: T;
  timestamp: string;
}

export function wrapResponse<T>(data: T): ApiResponse<T> {
  return {
    data,
    timestamp: new Date().toISOString(),
  };
}
