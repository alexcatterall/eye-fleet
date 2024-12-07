import Image from 'next/image';

export default function Logo({ className = "" }) {
  return (
    <div className={`${className}`}>
      <Image
        src="/eye_fleet_logo.png"
        alt="Eye Fleet Logo"
        width={200}
        height={200}
        className="rounded-lg"
      />
    </div>
  );
}
