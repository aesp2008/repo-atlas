import { cn } from "@/lib/utils";

interface CardProps {
  children: React.ReactNode;
  className?: string;
}

export function Card({ children, className }: CardProps) {
  return (
    <div className={cn("glass rounded-xl p-5 shadow-glow", className)}>
      {children}
    </div>
  );
}

export function CardTitle({ children, className }: CardProps) {
  return (
    <h3 className={cn("text-sm font-medium text-atlas-muted uppercase tracking-wider", className)}>
      {children}
    </h3>
  );
}

export function CardValue({ children, className }: CardProps) {
  return (
    <p className={cn("text-3xl font-bold mt-2 text-white", className)}>
      {children}
    </p>
  );
}
