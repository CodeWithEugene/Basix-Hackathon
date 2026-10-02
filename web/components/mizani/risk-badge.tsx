import { CircleCheck, Eye, Siren, TriangleAlert } from "lucide-react";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";
import { LEVEL_BADGE_CLASS, LEVEL_LABEL } from "@/lib/risk";
import type { RiskLevel } from "@/lib/types";
import { Badge } from "@/components/ui/badge";

const ICONS: Record<RiskLevel, typeof CircleCheck> = {
  normal: CircleCheck,
  watch: Eye,
  urgent: TriangleAlert,
  emergency: Siren,
};

const badgeVariants = cva("gap-1.5", {
  variants: {
    size: {
      sm: "text-xs",
      lg: "px-3 py-1 text-sm",
    },
  },
  defaultVariants: { size: "sm" },
});

export function RiskBadge({
  level,
  size,
  className,
}: {
  level: RiskLevel;
  size?: VariantProps<typeof badgeVariants>["size"];
  className?: string;
}) {
  const Icon = ICONS[level];
  return (
    <Badge
      className={cn(LEVEL_BADGE_CLASS[level], badgeVariants({ size }), className)}
      aria-label={`Risk level: ${LEVEL_LABEL[level]}`}
    >
      <Icon className="size-3.5" />
      {LEVEL_LABEL[level]}
    </Badge>
  );
}
