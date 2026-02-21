import AttendanceManagement from '@/components/AttendanceManagement';

export default function AttendancePage() {
  // Replace with actual event ID from URL params in production
  const eventId = 'demo-event-001';
  
  return <AttendanceManagement eventId={eventId} />;
}
