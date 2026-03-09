import { createClient } from "@/utils/supabase/server";
import Link from "next/link";
import { redirect } from "next/navigation";

interface DiaryEntry {
  diary_id: number;
  content: string;
  structured_data: {
    mood: string;
    mood_score: number;
    summary: string;
    tags: string[];
    key_events: string[];
  } | null;
  reflection: string | null;
  created_at: string;
}

export default async function DiaryDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const { data: { session } } = await supabase.auth.getSession();
  const token = session?.access_token;

  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/diary-entries/${id}`, {
    headers: { Authorization: `Bearer ${token}` },
    cache: "no-store",
  });

  if (!res.ok) redirect("/");
  const entry: DiaryEntry = await res.json();

  return (
    <div className="min-h-screen bg-zinc-50">
      <header className="flex items-center justify-between border-b border-zinc-200 bg-white px-6 py-4">
        <Link href="/" className="text-sm text-zinc-500 hover:text-zinc-900">
          ← 목록
        </Link>
        <span className="text-sm text-zinc-400">
          {new Date(entry.created_at).toLocaleDateString("ko-KR", {
            year: "numeric", month: "long", day: "numeric",
          })}
        </span>
        <div className="w-12" />
      </header>

      <main className="mx-auto max-w-2xl px-4 py-8 flex flex-col gap-6">
        {/* 일기 본문 */}
        <div className="rounded-xl bg-white p-6 shadow-sm">
          <p className="text-sm leading-7 text-zinc-800 whitespace-pre-wrap">{entry.content}</p>
        </div>

        {/* 감정 분석 */}
        {entry.structured_data && (
          <div className="rounded-xl bg-white p-6 shadow-sm">
            <h2 className="mb-3 text-sm font-semibold text-zinc-500">감정 분석</h2>
            <div className="flex items-center gap-3 mb-3">
              <span className="rounded-full bg-zinc-100 px-3 py-1 text-sm text-zinc-700">
                {entry.structured_data.mood}
              </span>
              <span className="text-sm text-zinc-500">
                {entry.structured_data.mood_score}/10
              </span>
            </div>
            <p className="text-sm text-zinc-600 mb-3">{entry.structured_data.summary}</p>
            <div className="flex flex-wrap gap-2">
              {entry.structured_data.tags.map((tag) => (
                <span key={tag} className="rounded-full bg-zinc-100 px-2 py-1 text-xs text-zinc-500">
                  #{tag}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* 리플렉션 */}
        <div className="rounded-xl bg-zinc-900 p-6 shadow-sm">
          <h2 className="mb-3 text-sm font-semibold text-zinc-400">리플렉션</h2>
          {entry.reflection ? (
            <p className="text-sm leading-7 text-zinc-100">{entry.reflection}</p>
          ) : (
            <p className="text-sm text-zinc-500 animate-pulse">리플렉션을 생성하고 있어요...</p>
          )}
        </div>
      </main>
    </div>
  );
}
