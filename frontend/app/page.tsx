import SessionRedirect from "@/components/auth/session-redirect";

export default function Home() {
  return (
    <SessionRedirect
      redirectIfAuthedTo="/dashboard"
      redirectIfUnauthedTo="/login"
    />
  );
}
