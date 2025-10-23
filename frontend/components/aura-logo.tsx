export function AuraLogo({ className = "" }: { className?: string }) {
  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <div className="relative">
        <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
          <span className="text-primary-foreground font-bold text-lg">A</span>
        </div>
        <div className="absolute -top-1 -right-1 w-3 h-3 bg-secondary rounded-full border-2 border-background"></div>
      </div>
      <span className="text-xl font-semibold text-primary">Aura Health</span>
    </div>
  )
}
