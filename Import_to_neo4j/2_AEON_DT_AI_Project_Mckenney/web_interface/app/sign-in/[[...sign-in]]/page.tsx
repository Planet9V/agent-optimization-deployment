import { SignIn } from '@clerk/nextjs';
import { dark } from '@clerk/themes';

export default function SignInPage() {
  return (
    <div className="relative min-h-screen w-full flex items-center justify-center overflow-hidden bg-dark text-white font-sans selection:bg-primary/30 selection:text-white">

      {/* Background Effects */}
      <div className="absolute inset-0 bg-grid opacity-20 pointer-events-none"></div>
      <div className="absolute inset-0 bg-gradient-to-b from-dark via-transparent to-dark pointer-events-none"></div>

      {/* Sphere Texture Overlay */}
      <div className="absolute inset-0 sphere-texture opacity-5 mix-blend-overlay pointer-events-none animate-spin-slow"></div>

      <div className="relative z-10 flex flex-col items-center gap-8 animate-in fade-in slide-in-from-bottom-8 duration-700">
        <div className="text-center space-y-2">
          <h1 className="text-3xl md:text-4xl font-bold uppercase tracking-tighter text-white">
            <span className="text-gradient-cyber">Psychohistory</span> Protocol
          </h1>
          <p className="text-gray-400 font-mono text-xs uppercase tracking-widest">
            Authorized Personnel Only
          </p>
        </div>

        <SignIn
          appearance={{
            baseTheme: dark,
            elements: {
              rootBox: "w-full",
              card: "bg-dark/80 backdrop-blur-md border border-primary/20 shadow-[0_0_40px_rgba(0,224,176,0.1)]",
              headerTitle: "text-white font-bold",
              headerSubtitle: "text-gray-400",
              socialButtonsBlockButton: "bg-surface border border-white/10 hover:bg-surface/80 text-white",
              formButtonPrimary: "bg-primary hover:bg-primary/90 text-dark font-bold",
              footerActionLink: "text-primary hover:text-primary/80",
              formFieldLabel: "text-gray-300",
              formFieldInput: "bg-surface border-white/10 text-white focus:border-primary/50",
            }
          }}
        />
      </div>
    </div>
  );
}
