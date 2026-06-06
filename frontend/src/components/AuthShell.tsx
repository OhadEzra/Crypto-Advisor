export default function AuthShell({ title, subtitle, children }: { title: string; subtitle: string; children: React.ReactNode }) {
  return <main className="min-h-screen grid place-items-center px-4">
    <section className="w-full max-w-md card">
      <div className="mb-8">
        <p className="badge inline-block mb-4">AI Crypto Advisor</p>
        <h1 className="text-4xl font-black">{title}</h1>
        <p className="mt-2 text-slate-300">{subtitle}</p>
      </div>
      {children}
    </section>
  </main>;
}
