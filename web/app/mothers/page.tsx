"use client";

import Link from "next/link";

import { useAgent } from "@/lib/api";
import { motherDisplay } from "@/lib/risk";
import type { Mother } from "@/lib/types";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

export default function MothersPage() {
  const { data, loading } = useAgent<{ mothers: Mother[] }>("facility", "/mothers");
  return (
    <div className="grid gap-4">
      <div>
        <h1 className="text-2xl font-semibold tracking-[-0.015em]">Mothers</h1>
        <p className="text-sm text-muted-foreground">
          Every mother the facility agent remembers, with her visits as atoms.
        </p>
      </div>
      {loading && <Skeleton className="h-40 w-full" />}
      <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
        {(data?.mothers ?? []).map((m) => (
          <Link key={m.id} href={`/mothers/${m.id}`}>
            <Card className="transition-colors hover:bg-accent/50">
              <CardHeader className="flex flex-row items-center gap-3">
                <Avatar>
                  <AvatarFallback>
                    {motherDisplay(m.id).slice(0, 2).toUpperCase()}
                  </AvatarFallback>
                </Avatar>
                <div>
                  <CardTitle className="text-base">{motherDisplay(m.id)}</CardTitle>
                  <CardDescription>
                    {m.age}y · G{m.gravida}P{m.para}
                    {m.ga_weeks != null ? ` · ${m.ga_weeks} weeks` : ""}
                  </CardDescription>
                </div>
              </CardHeader>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
