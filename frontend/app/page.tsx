import { createClient } from "@/utils/supabase/server";
import Link from "next/link";
import { redirect } from "next/navigation";
import LogoutButton from "./LogoutButton";

interface DiaryEntry {
  diary_id: number;
  content: string;
  structured_data: { mood: string; mood_score: number; summary: string } | null;
  reflection: string | null;
  created_at: string;
}

export default async function HomePage() {
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const { data: { session } } = await supabase.auth.getSession();
  const token = session?.access_token;

  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/diary-entries?limit=20`, {
    headers: { Authorization: `Bearer ${token}` },
    cache: "no-store",
  });

  const entries: DiaryEntry[] = res.ok ? await res.json() : [];

  return (
    <div className="min-h-screen bg-zinc-50">
      <header className="flex items-center justify-between border-b border-zinc-200 bg-white px-6 py-4">
        <h1 className="text-lg font-bold text-zinc-900">Demian 일기</h1>
        <div className="flex items-center gap-4">
          <Link
            href="/write"
            className="rounded-lg bg-zinc-900 px-4 py-2 text-sm font-medium text-white hover:bg-zinc-700"
          >
            + 새 일기
          </Link>
          <LogoutButton />
        </div>
      </header>

      <main className="mx-auto max-w-2xl px-4 py-8">
        {entries.length === 0 ? (
          <div className="text-center text-zinc-400 py-20">
            <p className="text-lg">아직 일기가 없어요.</p>
            <p className="text-sm mt-2">오늘의 이야기를 기록해보세요.</p>
          </div>
        ) : (
          <div className="flex flex-col gap-4">
            {entries.map((entry) => (
              <Link key={entry.diary_id} href={`/diary/${entry.diary_id}`}>
                <div className="rounded-xl bg-white p-5 shadow-sm hover:shadow-md transition">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs text-zinc-400">
                      {new Date(entry.created_at).toLocaleDateString("ko-KR", {
                        year: "numeric", month: "long", day: "numeric",
                      })}
                    </span>
                    {entry.structured_data && (
                      <span className="text-xs bg-zinc-100 text-zinc-600 px-2 py-1 rounded-full">
                        {entry.structured_data.mood} {entry.structured_data.mood_score}/10
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-zinc-700 line-clamp-2">{entry.content}</p>
                  {entry.structured_data?.summary && (
                    <p className="mt-2 text-xs text-zinc-400 italic">{entry.structured_data.summary}</p>
                  )}
                  {!entry.reflection && (
                    <p className="mt-2 text-xs text-blue-400">리플렉션 생성 중...</p>
                  )}
                </div>
              </Link>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
