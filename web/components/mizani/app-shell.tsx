"use client";

import * as React from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  ArrowRight,
  BookOpen,
  ClipboardList,
  HeartPulse,
  Inbox,
  Moon,
  Scale,
  Search,
  Stethoscope,
  Sun,
  Users,
} from "lucide-react";
import { useTheme } from "next-themes";

import { useAgent } from "@/lib/api";
import type { ReferralListItem } from "@/lib/types";
import { AgentHealth } from "@/components/mizani/agent-health";
import { ConnectivitySwitch } from "@/components/mizani/connectivity-switch";
import { ModeToggle } from "@/components/mizani/mode-toggle";
import { Alert, AlertDescription } from "@/components/ui/alert";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import { Button } from "@/components/ui/button";
import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
} from "@/components/ui/command";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Kbd } from "@/components/ui/kbd";
import { Separator } from "@/components/ui/separator";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarInset,
  SidebarMenu,
  SidebarMenuBadge,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";

const NAV = [
  { href: "/community", label: "Community Visit", icon: Stethoscope },
  { href: "/facility", label: "Facility Inbox", icon: Inbox, badge: true },
  { href: "/mothers", label: "Mothers", icon: Users },
  { href: "/audit", label: "Audit Log", icon: ClipboardList },
  { href: "/rules", label: "Rules", icon: BookOpen },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const inbox = useAgent<{ referrals: ReferralListItem[] }>(
    "facility",
    "/referrals",
    { pollMs: 5000 },
  );
  const pending = inbox.data?.referrals.filter(
    (r) => !r.reconciled_level,
  ).length;

  return (
    <SidebarProvider>
      <Sidebar variant="inset" collapsible="icon">
        <SidebarHeader>
          <SidebarMenu>
            <SidebarMenuItem>
              <SidebarMenuButton size="lg" render={<Link href="/" />}>
                <span className="flex size-8 items-center justify-center rounded-md bg-primary text-primary-foreground">
                  <Scale className="size-4" />
                </span>
                <span className="grid flex-1 text-left text-sm leading-tight">
                  <span className="font-semibold">Mizani</span>
                  <span className="text-xs text-muted-foreground">
                    Two Witnesses, One Referral
                  </span>
                </span>
              </SidebarMenuButton>
            </SidebarMenuItem>
            <SidebarMenuItem>
              <RoleSwitcher />
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarHeader>
        <SidebarContent>
          <SidebarGroup>
            <SidebarGroupLabel>Workflow</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {NAV.map((item) => (
                  <SidebarMenuItem key={item.href}>
                    <SidebarMenuButton
                      render={<Link href={item.href} />}
                      isActive={pathname.startsWith(item.href)}
                    >
                      <item.icon className="size-4" />
                      <span>{item.label}</span>
                    </SidebarMenuButton>
                    {item.badge && pending ? (
                      <SidebarMenuBadge>{pending}</SidebarMenuBadge>
                    ) : null}
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        </SidebarContent>
        <SidebarFooter>
          <div className="grid gap-3 px-2 pb-2">
            <ConnectivitySwitch />
            <Separator />
            <div className="flex items-center justify-between">
              <AgentHealth />
              <ModeToggle />
            </div>
          </div>
        </SidebarFooter>
      </Sidebar>
      <SidebarInset>
        <header className="flex h-12 items-center gap-3 border-b px-4">
          <SidebarTrigger />
          <Crumbs pathname={pathname} />
          <div className="ml-auto flex items-center gap-2">
            <CommandMenuButton />
          </div>
        </header>
        <Alert className="rounded-none border-x-0 border-t-0 py-1.5">
          <HeartPulse className="size-4" />
          <AlertDescription className="text-xs">
            Demo with synthetic data. Decision support, not diagnosis.
          </AlertDescription>
        </Alert>
        <main className="flex-1 p-4 md:p-6">{children}</main>
      </SidebarInset>
    </SidebarProvider>
  );
}

function RoleSwitcher() {
  const pathname = usePathname();
  const router = useRouter();
  const onFacility = pathname.startsWith("/facility");
  return (
    <DropdownMenu>
      <DropdownMenuTrigger
        render={
          <SidebarMenuButton variant="outline" className="w-full justify-between" />
        }
      >
        <span className="text-xs">
          {onFacility ? "Facility (Baraka, Nurse)" : "Community (Zawadi, CHP)"}
        </span>
        <ArrowRight className="size-3.5" />
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-64">
        <DropdownMenuLabel>Demo Roles</DropdownMenuLabel>
        <DropdownMenuItem onClick={() => router.push("/community")}>
          Community (Zawadi, CHP)
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => router.push("/facility")}>
          Facility (Baraka, Nurse)
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

const CRUMB_MAP: [RegExp, string[]][] = [
  [/^\/community/, ["Community Visit"]],
  [/^\/facility\/(.+)/, ["Facility Inbox", "Reconciliation"]],
  [/^\/facility/, ["Facility Inbox"]],
  [/^\/mothers\/(.+)/, ["Mothers", "Mother Memory"]],
  [/^\/mothers/, ["Mothers"]],
  [/^\/audit/, ["Audit Log"]],
  [/^\/rules/, ["Rules"]],
];

function Crumbs({ pathname }: { pathname: string }) {
  if (pathname === "/") {
    return (
      <Breadcrumb>
        <BreadcrumbList>
          <BreadcrumbItem>
            <BreadcrumbPage>Welcome</BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>
    );
  }
  const match = CRUMB_MAP.find(([re]) => re.test(pathname));
  const parts = match?.[1] ?? [];
  return (
    <Breadcrumb>
      <BreadcrumbList>
        <BreadcrumbItem>
          <BreadcrumbLink href="/">Mizani</BreadcrumbLink>
        </BreadcrumbItem>
        {parts.map((p, i) => (
          <React.Fragment key={p}>
            <BreadcrumbSeparator />
            <BreadcrumbItem>
              {i === parts.length - 1 ? (
                <BreadcrumbPage>{p}</BreadcrumbPage>
              ) : (
                <BreadcrumbLink href="#">{p}</BreadcrumbLink>
              )}
            </BreadcrumbItem>
          </React.Fragment>
        ))}
      </BreadcrumbList>
    </Breadcrumb>
  );
}

function CommandMenuButton() {
  const [open, setOpen] = React.useState(false);
  const router = useRouter();
  const { setTheme } = useTheme();

  React.useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((o) => !o);
      }
    };
    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, []);

  const go = (href: string) => {
    setOpen(false);
    router.push(href);
  };

  return (
    <>
      <Button variant="outline" size="sm" onClick={() => setOpen(true)}>
        <Search className="size-4" />
        <span className="hidden sm:inline">Search</span>
        <Kbd>⌘K</Kbd>
      </Button>
      <CommandDialog open={open} onOpenChange={setOpen}>
        <CommandInput placeholder="Type a command" />
        <CommandList>
          <CommandEmpty>No results.</CommandEmpty>
          <CommandGroup heading="Go To">
            <CommandItem onSelect={() => go("/facility")}>
              <Inbox className="size-4" /> Facility Inbox
            </CommandItem>
            <CommandItem onSelect={() => go("/community")}>
              <Stethoscope className="size-4" /> New Community Visit
            </CommandItem>
            <CommandItem onSelect={() => go("/mothers/M-AMINA")}>
              <Users className="size-4" /> Open Amina
            </CommandItem>
            <CommandItem onSelect={() => go("/audit")}>
              <ClipboardList className="size-4" /> Audit Log
            </CommandItem>
          </CommandGroup>
          <CommandSeparator />
          <CommandGroup heading="Display">
            <CommandItem onSelect={() => setTheme("light")}>
              <Sun className="size-4" /> Light Mode
            </CommandItem>
            <CommandItem onSelect={() => setTheme("dark")}>
              <Moon className="size-4" /> Dark Mode
            </CommandItem>
          </CommandGroup>
        </CommandList>
      </CommandDialog>
    </>
  );
}
