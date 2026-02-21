"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { colleges as initialColleges } from "@/lib/data";
import { images } from "@/lib/images";
import FounderSection from "@/components/FounderSection";
import Footer from "@/components/Footer";
import LoginModal from "@/components/LoginModal";
import EventParticipation from "@/components/EventParticipation";
import Events from "@/components/Events";
import { 
  ArrowRight, 
  Shield, 
  Brain, 
  FileText, 
  BarChart3, 
  Users, 
  Sparkles,
  TrendingUp,
  Clock,
  AlertTriangle,
  CheckCircle2,
  Search,
  X,
  ChevronRight,
  Zap,
  Target,
  Lightbulb,
  Rocket,
  Star,
  TrendingDown,
  Award,
  BookOpen,
  Calendar,
  MessageCircle,
  ThumbsUp,
  Eye,
  LineChart,
  PieChart,
  Activity,
  Wifi,
  Coffee,
  Car,
  GraduationCap,
  Building,
  MapPin,
  Hash,
  Flame,
  Hexagon,
  Circle,
  Triangle,
  Plus,
  LogIn,
  LogOut,
} from "lucide-react";

export default function HomePage() {
  const router = useRouter();
  const [colleges, setColleges] = useState(initialColleges);
  const [showCollegeModal, setShowCollegeModal] = useState(false);
  const [showAddCollegeModal, setShowAddCollegeModal] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [currentUser, setCurrentUser] = useState<any>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [scrollY, setScrollY] = useState(0);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [activeSection, setActiveSection] = useState(0);
  const [showEventsPage, setShowEventsPage] = useState(false);
  const [showEventParticipation, setShowEventParticipation] = useState(false);
  const [isMounted, setIsMounted] = useState(false);
  const heroRef = useRef<HTMLDivElement>(null);
  
  // Pre-computed particle data to avoid hydration mismatch
  const [particles, setParticles] = useState<{
    gold: Array<{ width: number; height: number; left: number; top: number; xMove: number; delay: number; duration: number }>;
    white: Array<{ left: number; top: number; delay: number; duration: number }>;
    green: Array<{ width: number; height: number; left: number; top: number; xMove: number; yMove: number; delay: number; duration: number }>;
    shapes: Array<{ left: number; top: number; delay: number; duration: number; shapeIndex: number; size: number }>;
  }>({ gold: [], white: [], green: [], shapes: [] });

  useEffect(() => {
    // Mark as mounted to prevent hydration mismatch
    setIsMounted(true);
    
    // Generate particle data client-side only
    const goldParticles = Array.from({ length: 30 }, () => ({
      width: Math.random() * 6 + 2,
      height: Math.random() * 6 + 2,
      left: Math.random() * 100,
      top: Math.random() * 100,
      xMove: Math.random() * 50 - 25,
      delay: Math.random() * 5,
      duration: Math.random() * 10 + 10,
    }));
    
    const whiteParticles = Array.from({ length: 60 }, () => ({
      left: Math.random() * 100,
      top: Math.random() * 100,
      delay: Math.random() * 5,
      duration: Math.random() * 8 + 5,
    }));
    
    const greenParticles = Array.from({ length: 20 }, () => ({
      width: Math.random() * 4 + 2,
      height: Math.random() * 4 + 2,
      left: Math.random() * 100,
      top: Math.random() * 100,
      xMove: Math.random() * 40 - 20,
      yMove: Math.random() * -80,
      delay: Math.random() * 4,
      duration: Math.random() * 8 + 8,
    }));
    
    const shapeParticles = Array.from({ length: 8 }, (_, i) => ({
      left: Math.random() * 100,
      top: Math.random() * 100,
      delay: Math.random() * 5,
      duration: 20 + Math.random() * 10,
      shapeIndex: i % 3,
      size: 60 + Math.random() * 40,
    }));
    
    setParticles({
      gold: goldParticles,
      white: whiteParticles,
      green: greenParticles,
      shapes: shapeParticles,
    });
    
    // Load colleges from localStorage
    const storedColleges = localStorage.getItem("campusMemoryColleges");
    if (storedColleges) {
      setColleges(JSON.parse(storedColleges));
    } else {
      localStorage.setItem("campusMemoryColleges", JSON.stringify(initialColleges));
    }

    // Load current user
    const storedUser = localStorage.getItem("campusMemoryCurrentUser");
    if (storedUser) {
      setCurrentUser(JSON.parse(storedUser));
    }

    const handleScroll = () => {
      setScrollY(window.scrollY);
      const sections = document.querySelectorAll('section');
      sections.forEach((section, index) => {
        const rect = section.getBoundingClientRect();
        if (rect.top <= 100 && rect.bottom >= 100) {
          setActiveSection(index);
        }
      });
    };
    
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };
    
    window.addEventListener("scroll", handleScroll);
    window.addEventListener("mousemove", handleMouseMove);
    return () => {
      window.removeEventListener("scroll", handleScroll);
      window.removeEventListener("mousemove", handleMouseMove);
    };
  }, []);

  const filteredColleges = colleges.filter(college =>
    college.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    college.city.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleCollegeSelect = (collegeId: string) => {
    router.push(`/colleges/${collegeId}`);
  };

  const handleLogin = (userData: any) => {
    setCurrentUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem("campusMemoryCurrentUser");
    setCurrentUser(null);
  };

  const handleAddCollege = (collegeData: any) => {
    const newCollege = {
      id: `custom-${Date.now()}`,
      ...collegeData,
      memoryIndex: 0,
      activeUsers: 0,
    };
    const updatedColleges = [...colleges, newCollege];
    setColleges(updatedColleges);
    localStorage.setItem("campusMemoryColleges", JSON.stringify(updatedColleges));
    setShowAddCollegeModal(false);
  };

  return (
    <main className="min-h-screen bg-white overflow-x-hidden">
      {/* Show Event Participation Page if active */}
      {showEventParticipation && (
        <div className="fixed inset-0 z-[100] bg-white overflow-y-auto">
          <EventParticipation />
          {/* Close Button */}
          <button
            onClick={() => setShowEventParticipation(false)}
            className="fixed top-6 right-6 z-[101] bg-gray-900 hover:bg-gray-800 text-white px-4 py-2 rounded-full transition-all shadow-lg flex items-center gap-2"
          >
            <X className="w-5 h-5" />
            Close
          </button>
        </div>
      )}
      
      {/* Show Events Page if active */}
      {showEventsPage && (
        <div className="fixed inset-0 z-[100] bg-slate-900">
          <Events 
            currentStudent={currentUser} 
            onLogin={() => setShowLoginModal(true)} 
          />
          {/* Close Button */}
          <button
            onClick={() => setShowEventsPage(false)}
            className="fixed top-6 right-6 z-[101] bg-white/10 hover:bg-white/20 backdrop-blur-lg text-white p-3 rounded-full transition-all"
          >
            <X className="w-6 h-6" />
          </button>
        </div>
      )}

      {/* Floating Navigation Progress Bar */}
      <div className="fixed top-0 left-0 right-0 z-50 h-1 bg-gray-200">
        <div 
          className="h-full bg-gradient-to-r from-[#D4AF37] via-[#F4D03F] to-[#D4AF37] transition-all duration-300"
          style={{ width: typeof window !== 'undefined' ? `${(scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100}%` : '0%' }}
        ></div>
      </div>

      {/* Floating Quick Stats */}
      <div className="fixed bottom-8 right-8 z-40 hidden lg:block space-y-4">
        {/* Stats Card */}
        <div className="bg-white/95 backdrop-blur-xl rounded-2xl shadow-2xl p-4 border border-gray-200 space-y-2 animate-slide-in-right"
>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#1E3A8A] to-[#1E40AF] flex items-center justify-center">
              <Eye className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="text-xs text-gray-500">Live Now</div>
              <div className="text-lg font-bold text-gray-900">127</div>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#D4AF37] to-[#B8941F] flex items-center justify-center">
              <Activity className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="text-xs text-gray-500">Active</div>
              <div className="text-lg font-bold text-gray-900">13 colleges</div>
            </div>
          </div>
        </div>
      </div>

      {/* SECTION 1: HERO - ULTRA ENHANCED */}
      <section ref={heroRef} className="relative min-h-screen flex items-center overflow-hidden">
        {/* Background Image with Overlay */}
        <div className="absolute inset-0">
          <img 
            src="https://i.ibb.co/5gHXTLy3/Chat-GPT-Image-Feb-7-2026-11-19-05-PM.png"
            alt="Campus Background"
            className="w-full h-full object-cover"
          />
          {/* Dark overlay for better text visibility - removed blue tint */}
          <div className="absolute inset-0 bg-black/40"></div>
          {/* Additional gradient overlay */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-black/40"></div>
        </div>

        {/* Enhanced Multi-Layer Particle System */}
        {isMounted && (
          <div className="absolute inset-0 z-10">
            {/* Large Golden Particles */}
            {particles.gold.map((particle, i) => (
              <motion.div
                key={`gold-${i}`}
                className="absolute rounded-full bg-[#D4AF37]"
                style={{
                  width: `${particle.width}px`,
                  height: `${particle.height}px`,
                  left: `${particle.left}%`,
                  top: `${particle.top}%`,
                }}
                animate={{
                  y: [0, -100, 0],
                  x: [0, particle.xMove, 0],
                  opacity: [0.2, 0.8, 0.2],
                  scale: [1, 1.5, 1],
                }}
                transition={{
                  duration: particle.duration,
                  repeat: Infinity,
                  delay: particle.delay,
                  ease: "easeInOut"
                }}
              ></motion.div>
            ))}
            
            {/* White Sparkle Particles */}
            {particles.white.map((particle, i) => (
              <motion.div
                key={`white-${i}`}
                className="absolute w-1 h-1 bg-white rounded-full"
                style={{
                  left: `${particle.left}%`,
                  top: `${particle.top}%`,
                }}
                animate={{
                  y: [0, -150],
                  opacity: [0, 1, 0],
                  scale: [0, 1, 0],
                }}
                transition={{
                  duration: particle.duration,
                  repeat: Infinity,
                  delay: particle.delay,
                  ease: "linear"
                }}
              ></motion.div>
            ))}

            {/* Green Emerald Particles */}
            {particles.green.map((particle, i) => (
              <motion.div
                key={`green-${i}`}
                className="absolute rounded-full bg-[#059669]"
                style={{
                  width: `${particle.width}px`,
                  height: `${particle.height}px`,
                  left: `${particle.left}%`,
                  top: `${particle.top}%`,
                }}
                animate={{
                  y: [0, particle.yMove, 0],
                  x: [0, particle.xMove, 0],
                  opacity: [0.3, 0.9, 0.3],
                }}
                transition={{
                  duration: particle.duration,
                  repeat: Infinity,
                  delay: particle.delay,
                  ease: "easeInOut"
                }}
              ></motion.div>
            ))}
          </div>
        )}

        {/* Floating Geometric Shapes */}
        {isMounted && (
          <div className="absolute inset-0 pointer-events-none z-10">
            {particles.shapes.map((particle, i) => {
              const shapes = [Hexagon, Circle, Triangle];
              const ShapeIcon = shapes[particle.shapeIndex];
              return (
                <motion.div
                  key={`shape-${i}`}
                  className="absolute text-white/10"
                  style={{
                    left: `${particle.left}%`,
                    top: `${particle.top}%`,
                  }}
                  animate={{
                    rotate: [0, 360],
                    scale: [1, 1.2, 1],
                    opacity: [0.1, 0.3, 0.1],
                  }}
                  transition={{
                    duration: particle.duration,
                    repeat: Infinity,
                    delay: particle.delay,
                  }}
                >
                  <ShapeIcon size={particle.size} strokeWidth={1} />
                </motion.div>
              );
            })}
          </div>
        )}

        {/* Subtle gradient overlay - no animated elements */}
        <div className="absolute inset-0 z-10">
          <div className="absolute inset-0 bg-gradient-to-br from-transparent via-black/10 to-transparent"></div>
        </div>

        <div className="relative z-20 mx-auto max-w-7xl px-6 lg:px-8">
          <div className="flex items-center justify-center min-h-[80vh] pt-12">
            {/* Center - Enhanced Content */}
            <motion.div 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, ease: "easeOut" }}
              className="space-y-8 max-w-4xl mx-auto text-center"
            >

              <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4, duration: 0.8 }}
              >
                <h1 className="font-serif text-2xl md:text-4xl lg:text-5xl font-bold text-white leading-tight mb-8 drop-shadow-2xl">
                  Your Campus Should Learn
                  <motion.span 
                    className="block bg-gradient-to-r from-[#D4AF37] via-[#F4D03F] to-[#D4AF37] bg-clip-text text-transparent bg-[length:200%_auto]"
                    animate={{
                      backgroundPosition: ["0% center", "200% center"],
                    }}
                    transition={{
                      duration: 3,
                      repeat: Infinity,
                      ease: "linear"
                    }}
                  >
                    From Its Past
                  </motion.span>
                </h1>
                <motion.div 
                  className="h-1.5 bg-gradient-to-r from-[#D4AF37] via-[#F4D03F] to-transparent rounded-full mx-auto"
                  initial={{ width: 0 }}
                  animate={{ width: 120 }}
                  transition={{ delay: 0.8, duration: 1 }}
                ></motion.div>
              </motion.div>

              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.6, duration: 0.8 }}
              >
                <p className="text-sm md:text-base text-white/95 leading-relaxed max-w-2xl mx-auto drop-shadow-lg">
                  Every year, students face the same problems. Faculty solve the same issues. 
                  <motion.span 
                    className="block mt-3 text-[#D4AF37] font-bold text-base md:text-lg"
                    animate={{ 
                      textShadow: [
                        "0 0 10px rgba(212, 175, 55, 0.5)",
                        "0 0 20px rgba(212, 175, 55, 0.8)",
                        "0 0 10px rgba(212, 175, 55, 0.5)"
                      ]
                    }}
                    transition={{ duration: 2, repeat: Infinity }}
                  >
                    What if your college could remember?
                  </motion.span>
                </p>
              </motion.div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* CTA Button Section - Above Founder */}
      <section className="relative -mt-32 py-6 bg-transparent z-50">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="flex justify-center relative z-50"
          >
            <div className="space-y-4">
              <div className="relative inline-block z-50">
                {/* Pulsing glow rings */}
                <motion.div
                  className="absolute -inset-4 bg-gradient-to-r from-[#D4AF37] via-[#F4D03F] to-[#D4AF37] rounded-full opacity-50 blur-xl pointer-events-none"
                  animate={{
                    scale: [1, 1.2, 1],
                    opacity: [0.5, 0.8, 0.5],
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                  }}
                ></motion.div>

                <motion.button
                  onClick={() => setShowCollegeModal(true)}
                  className="group relative inline-flex items-center gap-3 bg-gradient-to-r from-[#D4AF37] via-[#F4D03F] to-[#D4AF37] text-[#0F172A] px-8 py-5 rounded-full font-bold text-base md:text-lg shadow-2xl overflow-hidden whitespace-nowrap cursor-pointer z-50"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.98 }}
                >
                  {/* Animated background layers */}
                  <motion.div 
                    className="absolute inset-0 bg-gradient-to-r from-[#F4D03F] to-[#D4AF37]"
                    animate={{
                      opacity: [0, 0.5, 0],
                    }}
                    transition={{
                      duration: 2,
                      repeat: Infinity,
                    }}
                  ></motion.div>
                  
                  <motion.div 
                    className="absolute inset-0 bg-white/30"
                    initial={{ x: "-100%" }}
                    whileHover={{ x: "100%" }}
                    transition={{ duration: 0.6 }}
                  ></motion.div>

                  {/* Button content */}
                  <motion.div
                    className="relative z-10"
                    whileHover={{ rotate: 12, scale: 1.1 }}
                  >
                    <Rocket className="w-7 h-7" />
                  </motion.div>
                  <span className="relative z-10 text-base md:text-xl whitespace-nowrap">SELECT YOUR COLLEGE NOW</span>
                  <motion.div
                    className="relative z-10"
                    animate={{ x: [0, 5, 0] }}
                    transition={{ duration: 1.5, repeat: Infinity }}
                  >
                    <ArrowRight className="w-7 h-7" />
                  </motion.div>
                </motion.button>
              </div>
              
              {/* Event Planning Button */}
              <div className="relative inline-block z-50 mt-4">
                <motion.button
                  onClick={() => setShowEventParticipation(true)}
                  className="group relative inline-flex items-center gap-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white px-8 py-4 rounded-full font-bold text-base md:text-lg shadow-2xl overflow-hidden whitespace-nowrap cursor-pointer z-50"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <motion.div 
                    className="absolute inset-0 bg-white/20"
                    initial={{ x: "-100%" }}
                    whileHover={{ x: "100%" }}
                    transition={{ duration: 0.6 }}
                  ></motion.div>

                  <motion.div
                    className="relative z-10"
                    whileHover={{ rotate: 12, scale: 1.1 }}
                  >
                    <Calendar className="w-6 h-6" />
                  </motion.div>
                  <span className="relative z-10 text-base md:text-lg whitespace-nowrap">Plan an Event? See Past Insights</span>
                  <motion.div
                    className="relative z-10"
                    animate={{ x: [0, 5, 0] }}
                    transition={{ duration: 1.5, repeat: Infinity }}
                  >
                    <Lightbulb className="w-6 h-6" />
                  </motion.div>
                </motion.button>
              </div>

              <motion.p 
                className="text-xs text-gray-600 italic flex items-center justify-center gap-2"
                animate={{ opacity: [0.6, 1, 0.6] }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                <Star className="w-3 h-3 text-[#D4AF37]" />
                <span>Free demo dashboard • No sign-up required • Instant access</span>
              </motion.p>
            </div>
          </motion.div>
        </div>
      </section>

      {/* FOUNDER SECTION - Added Here */}
      <FounderSection />

      {/* INTERACTIVE 3D FEATURES SHOWCASE */}
      <section className="relative py-32 bg-white overflow-hidden">
        {/* Decorative Background Elements */}
        <div className="absolute top-0 left-0 w-full h-full overflow-hidden">
          <motion.div 
            className="absolute -top-40 -left-40 w-96 h-96 bg-[#1E3A8A]/5 rounded-full blur-3xl"
            animate={{
              scale: [1, 1.2, 1],
              x: [0, 50, 0],
              y: [0, 30, 0],
            }}
            transition={{
              duration: 20,
              repeat: Infinity,
            }}
          />
          <motion.div 
            className="absolute -bottom-40 -right-40 w-96 h-96 bg-[#D4AF37]/5 rounded-full blur-3xl"
            animate={{
              scale: [1, 1.3, 1],
              x: [0, -50, 0],
              y: [0, -30, 0],
            }}
            transition={{
              duration: 25,
              repeat: Infinity,
            }}
          />
        </div>

        <div className="relative z-10 mx-auto max-w-7xl px-6 lg:px-8">
          {/* Redesigned Header Section */}
          <div className="relative mb-20">
            {/* Decorative Background Elements */}
            <div className="absolute inset-0 -z-10">
              {/* Floating Orbs */}
              <motion.div
                className="absolute top-20 left-10 w-72 h-72 bg-gradient-to-br from-[#D4AF37]/20 to-[#F4D03F]/10 rounded-full blur-3xl"
                animate={{
                  y: [-20, 20, -20],
                  x: [-10, 10, -10],
                  scale: [1, 1.1, 1],
                }}
                transition={{
                  duration: 8,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              />
              <motion.div
                className="absolute top-10 right-20 w-96 h-96 bg-gradient-to-br from-[#059669]/20 to-[#10B981]/10 rounded-full blur-3xl"
                animate={{
                  y: [20, -20, 20],
                  x: [10, -10, 10],
                  scale: [1.1, 1, 1.1],
                }}
                transition={{
                  duration: 10,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              />
              
              {/* Geometric Shapes */}
              <motion.div
                className="absolute top-32 right-32 text-[#D4AF37]/10"
                animate={{ rotate: 360 }}
                transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
              >
                <Hexagon className="w-32 h-32" />
              </motion.div>
              <motion.div
                className="absolute bottom-10 left-1/4 text-[#059669]/10"
                animate={{ rotate: -360 }}
                transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
              >
                <Target className="w-24 h-24" />
              </motion.div>
            </div>

            {/* Content Container */}
            <div className="grid lg:grid-cols-2 gap-16 items-center">
              {/* Left Side - Main Heading */}
              <motion.div
                initial={{ opacity: 0, x: -50 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.8 }}
                className="relative"
              >
                {/* Badge */}
                <motion.div 
                  className="inline-flex items-center gap-2 px-4 py-2 bg-white shadow-lg rounded-full mb-8 border-2 border-[#D4AF37]/20"
                  whileHover={{ scale: 1.05, y: -2 }}
                  transition={{ type: "spring", stiffness: 300 }}
                >
                  <motion.div
                    animate={{ rotate: [0, 15, -15, 0] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  >
                    <Sparkles className="w-5 h-5 text-[#D4AF37]" />
                  </motion.div>
                  <span className="text-sm font-bold text-[#1E3A8A]">THE FUTURE OF CAMPUS MANAGEMENT</span>
                  <motion.div
                    animate={{ rotate: [0, -15, 15, 0] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  >
                    <Zap className="w-5 h-5 text-[#059669]" />
                  </motion.div>
                </motion.div>
                
                {/* Main Title */}
                <h2 className="relative mb-6">
                  <span className="block font-serif text-6xl md:text-7xl lg:text-8xl font-black text-[#1E3A8A] leading-none mb-4">
                    Everything
                  </span>
                  <span className="block font-serif text-6xl md:text-7xl lg:text-8xl font-black leading-none">
                    <span className="bg-gradient-to-r from-[#D4AF37] via-[#F4D03F] to-[#D4AF37] bg-clip-text text-transparent animate-gradient bg-[length:200%_auto]">
                      Your Campus
                    </span>
                  </span>
                  <span className="block font-serif text-6xl md:text-7xl lg:text-8xl font-black text-[#059669] leading-none mt-4">
                    Needs
                  </span>
                  
                  {/* Decorative Elements */}
                  <motion.div
                    className="absolute -top-6 -right-6 text-[#D4AF37]"
                    animate={{ 
                      rotate: [0, 10, -10, 0],
                      scale: [1, 1.1, 1]
                    }}
                    transition={{ duration: 3, repeat: Infinity }}
                  >
                    <Star className="w-16 h-16 fill-current" />
                  </motion.div>
                  <motion.div
                    className="absolute bottom-0 -left-4 text-[#059669]"
                    animate={{ 
                      y: [0, -10, 0]
                    }}
                    transition={{ duration: 2, repeat: Infinity }}
                  >
                    <Circle className="w-12 h-12 opacity-30" />
                  </motion.div>
                </h2>

                {/* Decorative Line */}
                <motion.div 
                  className="w-24 h-1.5 bg-gradient-to-r from-[#D4AF37] to-[#059669] rounded-full mb-6"
                  initial={{ width: 0 }}
                  whileInView={{ width: 96 }}
                  viewport={{ once: true }}
                  transition={{ duration: 1, delay: 0.3 }}
                />
              </motion.div>

              {/* Right Side - Subheading & Description */}
              <motion.div
                initial={{ opacity: 0, x: 50 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.8, delay: 0.2 }}
                className="relative"
              >
                {/* Glass Card Effect */}
                <div className="relative bg-white/50 backdrop-blur-sm rounded-3xl p-10 shadow-2xl border border-white/20">
                  {/* Gradient Border Effect */}
                  <div className="absolute inset-0 bg-gradient-to-br from-[#D4AF37]/20 via-transparent to-[#059669]/20 rounded-3xl" />
                  
                  <div className="relative z-10">
                    {/* Subtitle */}
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: 0.4 }}
                    >
                      <h3 className="font-serif text-4xl md:text-5xl font-bold text-[#1E3A8A] mb-6 leading-tight">
                        In One{" "}
                        <span className="relative inline-block">
                          <span className="bg-gradient-to-r from-[#D4AF37] to-[#059669] bg-clip-text text-transparent">
                            Intelligent
                          </span>
                          <motion.span
                            className="absolute -bottom-2 left-0 right-0 h-1 bg-gradient-to-r from-[#D4AF37] to-[#059669]"
                            initial={{ scaleX: 0 }}
                            whileInView={{ scaleX: 1 }}
                            viewport={{ once: true }}
                            transition={{ delay: 0.6, duration: 0.8 }}
                          />
                        </span>{" "}
                        Platform
                      </h3>
                    </motion.div>
                    
                    {/* Description */}
                    <motion.p 
                      className="text-xl text-gray-700 leading-relaxed mb-8"
                      initial={{ opacity: 0, y: 20 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: 0.5 }}
                    >
                      Transform scattered campus data into{" "}
                      <span className="font-bold text-[#D4AF37]">actionable intelligence</span>.
                      Harness the power of{" "}
                      <span className="font-bold text-[#059669]">collective wisdom</span>{" "}
                      to build a smarter, more connected institution.
                    </motion.p>

                    {/* Feature Pills */}
                    <motion.div 
                      className="flex flex-wrap gap-3"
                      initial={{ opacity: 0, y: 20 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: 0.6 }}
                    >
                      {[
                        { icon: Brain, text: "AI-Powered", color: "from-[#3B82F6] to-[#2563EB]" },
                        { icon: Zap, text: "Real-Time", color: "from-[#F59E0B] to-[#D97706]" },
                        { icon: Shield, text: "Secure", color: "from-[#10B981] to-[#059669]" }
                      ].map((item, index) => (
                        <motion.div
                          key={index}
                          className={`group flex items-center gap-2 px-4 py-2 bg-gradient-to-r ${item.color} text-white rounded-full shadow-lg`}
                          whileHover={{ scale: 1.05, y: -2 }}
                          transition={{ type: "spring", stiffness: 300 }}
                        >
                          <item.icon className="w-4 h-4" />
                          <span className="text-sm font-semibold">{item.text}</span>
                        </motion.div>
                      ))}
                    </motion.div>
                  </div>

                  {/* Decorative Corner Elements */}
                  <div className="absolute -top-3 -right-3 w-20 h-20 bg-gradient-to-br from-[#D4AF37] to-[#F4D03F] rounded-full opacity-20 blur-xl" />
                  <div className="absolute -bottom-3 -left-3 w-16 h-16 bg-gradient-to-br from-[#059669] to-[#10B981] rounded-full opacity-20 blur-xl" />
                </div>
              </motion.div>
            </div>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: <Brain className="w-12 h-12" />,
                title: "AI-Powered Memory",
                description: "Machine learning algorithms that learn from every problem, solution, and interaction",
                color: "from-[#3B82F6] to-[#2563EB]",
                highlight: "#3B82F6",
              },
              {
                icon: <AlertTriangle className="w-12 h-12" />,
                title: "Smart Warnings",
                description: "Predictive alerts before issues escalate, based on historical patterns",
                color: "from-[#F59E0B] to-[#D97706]",
                highlight: "#F59E0B",
              },
              {
                icon: <BarChart3 className="w-12 h-12" />,
                title: "Visual Analytics",
                description: "Beautiful dashboards that turn complex data into actionable insights",
                color: "from-[#10B981] to-[#059669]",
                highlight: "#10B981",
              },
              {
                icon: <Users className="w-12 h-12" />,
                title: "Crowd Wisdom",
                description: "Collective intelligence from students, faculty, and staff",
                color: "from-[#8B5CF6] to-[#7C3AED]",
                highlight: "#8B5CF6",
              },
              {
                icon: <Target className="w-12 h-12" />,
                title: "Pattern Recognition",
                description: "Identifies recurring issues and suggests proactive solutions",
                color: "from-[#EC4899] to-[#DB2777]",
                highlight: "#EC4899",
              },
              {
                icon: <Sparkles className="w-12 h-12" />,
                title: "Gamification",
                description: "Reward students for contributing knowledge and solving problems",
                color: "from-[#D4AF37] to-[#B8941F]",
                highlight: "#D4AF37",
              },
            ].map((feature, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: idx * 0.1 }}
                whileHover={{ 
                  y: -10, 
                  rotateY: 5,
                  transition: { duration: 0.3 }
                }}
                className="group relative"
                style={{ transformStyle: "preserve-3d" }}
              >
                {/* Glow effect on hover */}
                <div 
                  className="absolute -inset-2 rounded-3xl blur-xl opacity-0 group-hover:opacity-70 transition-opacity duration-500"
                  style={{
                    background: `linear-gradient(135deg, ${feature.highlight}40, ${feature.highlight}20)`,
                  }}
                />

                {/* Card */}
                <div className="relative h-full bg-white rounded-2xl shadow-lg border-2 border-gray-100 p-8 overflow-hidden group-hover:border-transparent transition-all duration-300">
                  {/* Animated gradient overlay */}
                  <div 
                    className={`absolute inset-0 bg-gradient-to-br ${feature.color} opacity-0 group-hover:opacity-5 transition-opacity duration-500`}
                  />

                  {/* Shimmer effect */}
                  <motion.div
                    className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-0 group-hover:opacity-30"
                    animate={{
                      x: ["-100%", "200%"],
                    }}
                    transition={{
                      duration: 1.5,
                      repeat: Infinity,
                      repeatDelay: 1,
                    }}
                  />

                  {/* Content */}
                  <div className="relative z-10">
                    {/* Icon */}
                    <motion.div 
                      className={`inline-flex p-4 rounded-2xl bg-gradient-to-br ${feature.color} text-white mb-6 shadow-lg`}
                      whileHover={{ 
                        rotate: [0, -10, 10, -10, 0],
                        scale: 1.1,
                      }}
                      transition={{ duration: 0.5 }}
                      style={{
                        boxShadow: `0 10px 30px ${feature.highlight}40`,
                      }}
                    >
                      {feature.icon}
                    </motion.div>

                    {/* Title */}
                    <h3 className="text-2xl font-bold text-gray-900 mb-4 group-hover:text-[#1E3A8A] transition-colors">
                      {feature.title}
                    </h3>

                    {/* Description */}
                    <p className="text-gray-600 leading-relaxed mb-6">
                      {feature.description}
                    </p>

                    {/* Interactive arrow */}
                    <motion.div 
                      className="flex items-center gap-2 text-sm font-semibold"
                      style={{ color: feature.highlight }}
                    >
                      <span>Learn more</span>
                      <motion.div
                        animate={{
                          x: [0, 5, 0],
                        }}
                        transition={{
                          duration: 1.5,
                          repeat: Infinity,
                        }}
                      >
                        <ArrowRight className="w-4 h-4" />
                      </motion.div>
                    </motion.div>
                  </div>

                  {/* Corner accent */}
                  <div 
                    className="absolute top-0 right-0 w-20 h-20 opacity-10 rounded-bl-full"
                    style={{
                      background: `linear-gradient(135deg, ${feature.highlight}, transparent)`,
                    }}
                  />
                </div>
              </motion.div>
            ))}
          </div>

          {/* Bottom CTA */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.5 }}
            className="text-center mt-16"
          >
            <motion.button
              onClick={() => setShowCollegeModal(true)}
              className="group inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-[#1E3A8A] to-[#1E40AF] text-white rounded-full font-semibold text-lg shadow-xl hover:shadow-2xl transition-all"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.98 }}
            >
              <span>Explore All Features</span>
              <motion.div
                animate={{ x: [0, 5, 0] }}
                transition={{ duration: 1.5, repeat: Infinity }}
              >
                <ChevronRight className="w-5 h-5" />
              </motion.div>
            </motion.button>
          </motion.div>
        </div>
      </section>

      {/* SECTION 2: THE PAIN */}
      <section className="py-32 bg-gradient-to-b from-white via-gray-50 to-white relative overflow-hidden">
        {/* Decorative Elements */}
        <div className="absolute top-20 left-10 w-72 h-72 bg-[#1E3A8A]/5 rounded-full blur-3xl"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-[#059669]/5 rounded-full blur-3xl"></div>

        <div className="mx-auto max-w-7xl px-6 lg:px-8 relative z-10">
          {/* Redesigned Problem Header */}
          <div className="relative mb-24">
            {/* Background Visual Elements */}
            <div className="absolute inset-0 -z-10">
              <motion.div
                className="absolute top-0 left-1/4 w-64 h-64 bg-gradient-to-br from-red-500/20 to-orange-500/10 rounded-full blur-3xl"
                animate={{
                  scale: [1, 1.2, 1],
                  opacity: [0.3, 0.5, 0.3],
                }}
                transition={{ duration: 4, repeat: Infinity }}
              />
              <motion.div
                className="absolute top-20 right-1/4 w-80 h-80 bg-gradient-to-br from-yellow-500/20 to-red-500/10 rounded-full blur-3xl"
                animate={{
                  scale: [1.2, 1, 1.2],
                  opacity: [0.3, 0.5, 0.3],
                }}
                transition={{ duration: 5, repeat: Infinity, delay: 0.5 }}
              />
            </div>

            {/* Main Content Container */}
            <div className="grid lg:grid-cols-2 gap-16 items-center">
              {/* Left Side - Dramatic Heading */}
              <motion.div
                initial={{ opacity: 0, x: -50 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.8 }}
                className="relative"
              >
                {/* Animated Badge */}
                <motion.div
                  className="inline-flex items-center gap-2 px-5 py-3 bg-gradient-to-r from-red-500 to-orange-500 text-white rounded-full mb-8 shadow-xl"
                  whileHover={{ scale: 1.05, rotate: 2 }}
                >
                  <motion.div
                    animate={{ rotate: [0, 20, -20, 0] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  >
                    <AlertTriangle className="w-5 h-5" />
                  </motion.div>
                  <span className="font-bold text-sm tracking-wider">THE CAMPUS CRISIS</span>
                </motion.div>

                {/* Main Title - Split & Styled */}
                <h2 className="relative mb-8">
                  <span className="block font-serif text-5xl md:text-6xl lg:text-7xl font-black text-[#1E3A8A] leading-tight mb-3">
                    The Cycle Of
                  </span>
                  <span className="block font-serif text-6xl md:text-7xl lg:text-8xl font-black leading-none">
                    <span className="bg-gradient-to-r from-red-600 via-orange-600 to-red-600 bg-clip-text text-transparent animate-gradient bg-[length:200%_auto]">
                      Forgotten
                    </span>
                  </span>
                  <span className="block font-serif text-5xl md:text-6xl lg:text-7xl font-black text-[#1E3A8A] leading-tight mt-3">
                    Lessons
                  </span>

                  {/* Decorative Warning Icons */}
                  <motion.div
                    className="absolute -top-6 -right-8 text-red-500"
                    animate={{
                      rotate: [0, 15, -15, 0],
                      scale: [1, 1.2, 1],
                    }}
                    transition={{ duration: 2.5, repeat: Infinity }}
                  >
                    <AlertTriangle className="w-20 h-20 fill-red-100" />
                  </motion.div>
                </h2>

                {/* Animated Accent Line */}
                <motion.div
                  className="w-32 h-2 bg-gradient-to-r from-red-600 to-orange-600 rounded-full mb-6"
                  initial={{ width: 0 }}
                  whileInView={{ width: 128 }}
                  viewport={{ once: true }}
                  transition={{ duration: 1, delay: 0.3 }}
                />

                {/* Impactful Tagline */}
                <motion.p
                  className="text-2xl md:text-3xl font-serif text-gray-700 leading-relaxed"
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: 0.4 }}
                >
                  When history repeats because{" "}
                  <span className="font-bold text-red-600 italic">nobody was listening</span>
                </motion.p>
              </motion.div>

              {/* Right Side - Problem Visualization */}
              <motion.div
                initial={{ opacity: 0, x: 50 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.8, delay: 0.2 }}
                className="relative"
              >
                {/* Glass Card with Problems */}
                <div className="relative bg-white/80 backdrop-blur-lg rounded-3xl p-8 shadow-2xl border-2 border-red-200">
                  {/* Gradient Overlay */}
                  <div className="absolute inset-0 bg-gradient-to-br from-red-50/50 via-orange-50/30 to-yellow-50/50 rounded-3xl" />

                  <div className="relative z-10">
                    {/* Section Label */}
                    <div className="flex items-center gap-3 mb-8">
                      <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-red-500 to-orange-500 flex items-center justify-center shadow-lg">
                        <TrendingDown className="w-6 h-6 text-white" />
                      </div>
                      <div>
                        <h3 className="text-2xl font-bold text-[#1E3A8A]">The Pattern</h3>
                        <p className="text-sm text-red-600 font-semibold">Repeating Endlessly</p>
                      </div>
                    </div>

                    {/* Rotating Problem Cards */}
                    <div className="space-y-4">
                      {[
                        { year: "2022", problem: "WiFi dead spots in library", icon: Wifi, color: "from-red-500 to-red-600" },
                        { year: "2023", problem: "Same WiFi issues persist", icon: Wifi, color: "from-orange-500 to-orange-600" },
                        { year: "2024", problem: "Still no solution found", icon: Wifi, color: "from-yellow-500 to-yellow-600" },
                        { year: "2025", problem: "Problem complaints flood in", icon: AlertTriangle, color: "from-red-600 to-orange-600" },
                      ].map((item, idx) => (
                        <motion.div
                          key={idx}
                          className="group relative p-4 rounded-xl bg-white shadow-lg border-2 border-gray-100 hover:border-red-300 transition-all"
                          initial={{ opacity: 0, x: -20 }}
                          whileInView={{ opacity: 1, x: 0 }}
                          viewport={{ once: true }}
                          transition={{ delay: 0.5 + idx * 0.1 }}
                          whileHover={{ x: 10, scale: 1.02 }}
                        >
                          <div className="flex items-center gap-4">
                            <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${item.color} flex items-center justify-center flex-shrink-0`}>
                              <item.icon className="w-5 h-5 text-white" />
                            </div>
                            <div className="flex-1">
                              <div className="flex items-center gap-2 mb-1">
                                <span className="text-xs font-bold text-gray-500">{item.year}</span>
                                <div className="h-1 w-1 rounded-full bg-gray-300" />
                                <span className="text-xs text-red-600 font-semibold">BATCH {idx + 1}</span>
                              </div>
                              <p className="text-sm font-semibold text-gray-800">{item.problem}</p>
                            </div>
                            <motion.div
                              className="text-red-400"
                              animate={{ rotate: [0, 360] }}
                              transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                            >
                              <TrendingDown className="w-5 h-5" />
                            </motion.div>
                          </div>
                        </motion.div>
                      ))}
                    </div>

                    {/* Impact Statement */}
                    <motion.div
                      className="mt-6 p-5 bg-gradient-to-r from-red-500 to-orange-500 rounded-xl shadow-xl"
                      initial={{ opacity: 0, y: 20 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: 1 }}
                    >
                      <div className="flex items-center gap-3 text-white">
                        <motion.div
                          animate={{ scale: [1, 1.2, 1] }}
                          transition={{ duration: 2, repeat: Infinity }}
                        >
                          <AlertTriangle className="w-6 h-6" />
                        </motion.div>
                        <p className="text-sm font-bold">
                          Average student wastes <span className="text-xl">200+ hours/year</span> solving already-solved problems
                        </p>
                      </div>
                    </motion.div>
                  </div>

                  {/* Corner Decorations */}
                  <div className="absolute -top-4 -right-4 w-24 h-24 bg-gradient-to-br from-red-400 to-orange-400 rounded-full opacity-20 blur-2xl" />
                  <div className="absolute -bottom-4 -left-4 w-20 h-20 bg-gradient-to-br from-yellow-400 to-red-400 rounded-full opacity-20 blur-2xl" />
                </div>
              </motion.div>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-12">
            {/* Student Struggles */}
            <div className="space-y-4 animate-slide-in-left">
              <div className="sticky top-24">
                <div className="bg-gradient-to-br from-red-50 to-orange-50 rounded-3xl p-8 border-2 border-red-200 shadow-xl">
                  <div className="flex items-center gap-4 mb-6">
                    <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-red-500 to-orange-500 flex items-center justify-center shadow-lg">
                      <Users className="w-8 h-8 text-white" />
                    </div>
                    <div>
                      <h3 className="font-serif text-2xl font-bold text-[#1E3A8A]">
                        Every Year, Students Face
                      </h3>
                      <p className="text-sm text-red-600 font-semibold">The Same Old Problems</p>
                    </div>
                  </div>

                  <div className="space-y-3">
                    {[
                      { icon: <Clock />, title: "TIMETABLE CHAOS", desc: "Same clashes, new batch", severity: "high" },
                      { icon: <Car />, title: "PARKING NIGHTMARES", desc: "Fest after fest", severity: "high" },
                      { icon: <BookOpen />, title: "RESOURCE SHORTAGES", desc: "Lab equipment? Library seats?", severity: "medium" },
                      { icon: <Calendar />, title: "EVENT MISHAPS", desc: "Learned nothing from last year", severity: "medium" },
                      { icon: <Building />, title: "HOSTEL ISSUES", desc: "Food, maintenance, WiFi", severity: "high" },
                      { icon: <Wifi />, title: "CONNECTIVITY FAILS", desc: "Same spots, zero signal", severity: "medium" },
                      { icon: <Coffee />, title: "CANTEEN COMPLAINTS", desc: "Quality? Quantity? Both!", severity: "low" },
                    ].map((item, idx) => (
                      <div 
                        key={idx}
                        className="group flex items-start gap-4 p-4 rounded-2xl bg-white hover:bg-gradient-to-r hover:from-white hover:to-red-50 hover:shadow-lg transition-all duration-300 border border-transparent hover:border-red-200"
                      >
                        <div className={`flex-shrink-0 w-12 h-12 rounded-xl ${
                          item.severity === 'high' ? 'bg-red-100' : item.severity === 'medium' ? 'bg-orange-100' : 'bg-yellow-100'
                        } flex items-center justify-center group-hover:scale-110 group-hover:rotate-12 transition-all duration-300`}>
                          <div className={`${
                            item.severity === 'high' ? 'text-red-600' : item.severity === 'medium' ? 'text-orange-600' : 'text-yellow-600'
                          }`}>
                            {item.icon}
                          </div>
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <h4 className="font-bold text-gray-900 text-sm">{item.title}</h4>
                            <span className={`text-xs px-2 py-0.5 rounded-full ${
                              item.severity === 'high' ? 'bg-red-100 text-red-700' : 
                              item.severity === 'medium' ? 'bg-orange-100 text-orange-700' : 'bg-yellow-100 text-yellow-700'
                            }`}>
                              {item.severity}
                            </span>
                          </div>
                          <p className="text-sm text-gray-600">{item.desc}</p>
                        </div>
                        <X className="w-5 h-5 text-red-400 opacity-0 group-hover:opacity-100 transition-opacity" />
                      </div>
                    ))}
                  </div>

                  <div className="mt-6 p-4 bg-red-100 rounded-xl border border-red-200">
                    <p className="text-sm text-red-800 font-semibold text-center">
                      💔 Average student wastes 200+ hours/year on repeated problems
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Faculty Frustrations */}
            <div className="space-y-4 animate-slide-in-right">
              <div className="sticky top-24">
                <div className="bg-gradient-to-br from-orange-50 to-yellow-50 rounded-3xl p-8 border-2 border-orange-200 shadow-xl">
                  <div className="flex items-center gap-4 mb-6">
                    <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-orange-500 to-yellow-500 flex items-center justify-center shadow-lg">
                      <FileText className="w-8 h-8 text-white" />
                    </div>
                    <div>
                      <h3 className="font-serif text-2xl font-bold text-[#1E3A8A]">
                        Every Semester, Faculty Encounter
                      </h3>
                      <p className="text-sm text-orange-600 font-semibold">The Same Old Bottlenecks</p>
                    </div>
                  </div>

                  <div className="space-y-3">
                    {[
                      { icon: <TrendingDown />, title: "REPEATING MISTAKES", desc: "Same policy failures", impact: "critical" },
                      { icon: <Clock />, title: "ADMIN BOTTLENECKS", desc: "Manual processes, again", impact: "high" },
                      { icon: <Target />, title: "RESOURCE MISALLOCATION", desc: "Budgeting blind", impact: "high" },
                      { icon: <MessageCircle />, title: "COMMUNICATION GAPS", desc: "Siloed departments", impact: "medium" },
                      { icon: <BarChart3 />, title: "NO DATA INSIGHTS", desc: "Decisions based on gut feel", impact: "critical" },
                      { icon: <AlertTriangle />, title: "CRISIS MANAGEMENT", desc: "Always reactive, never proactive", impact: "high" },
                    ].map((item, idx) => (
                      <div 
                        key={idx}
                        className="group flex items-start gap-4 p-4 rounded-2xl bg-white hover:bg-gradient-to-r hover:from-white hover:to-orange-50 hover:shadow-lg transition-all duration-300 border border-transparent hover:border-orange-200"
                      >
                        <div className={`flex-shrink-0 w-12 h-12 rounded-xl ${
                          item.impact === 'critical' ? 'bg-red-100' : item.impact === 'high' ? 'bg-orange-100' : 'bg-yellow-100'
                        } flex items-center justify-center group-hover:scale-110 group-hover:-rotate-12 transition-all duration-300`}>
                          <div className={`${
                            item.impact === 'critical' ? 'text-red-600' : item.impact === 'high' ? 'text-orange-600' : 'text-yellow-600'
                          }`}>
                            {item.icon}
                          </div>
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <h4 className="font-bold text-gray-900 text-sm">{item.title}</h4>
                            <span className={`text-xs px-2 py-0.5 rounded-full ${
                              item.impact === 'critical' ? 'bg-red-100 text-red-700' : 
                              item.impact === 'high' ? 'bg-orange-100 text-orange-700' : 'bg-yellow-100 text-yellow-700'
                            }`}>
                              {item.impact}
                            </span>
                          </div>
                          <p className="text-sm text-gray-600">{item.desc}</p>
                        </div>
                        <AlertTriangle className="w-5 h-5 text-orange-400 opacity-0 group-hover:opacity-100 transition-opacity" />
                      </div>
                    ))}
                  </div>

                  <div className="mt-6 p-4 bg-orange-100 rounded-xl border border-orange-200">
                    <p className="text-sm text-orange-800 font-semibold text-center">
                      📊 Institutions lose ₹50L+/year on preventable problems
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Bottom Impact Statement */}
          <div className="mt-16 text-center">
            <div className="inline-block p-8 bg-gradient-to-br from-gray-900 to-gray-800 rounded-3xl shadow-2xl">
              <p className="text-2xl md:text-3xl font-serif font-bold text-white mb-2">
                "If only we knew this last year..."
              </p>
              <p className="text-gray-400">- Every student ever</p>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION 3: GRADUATION SHOULDN'T MEAN AMNESIA - 2022 to 2026 */}
      <section className="py-32 bg-gradient-to-br from-[#1E3A8A]/5 via-purple-50 to-[#059669]/5 relative overflow-hidden">
        {/* Animated Background */}
        {isMounted && (
          <div className="absolute inset-0">
            {Array.from({ length: 20 }, (_, i) => {
              const left = (i * 5.26) % 100;
              const top = (i * 7.89) % 100;
              const delay = (i * 0.25) % 5;
              const duration = 10 + (i * 0.5) % 10;
              return (
                <div
                  key={i}
                  className="absolute w-2 h-2 bg-gray-300 rounded-full animate-float-slow"
                  style={{
                    left: `${left}%`,
                    top: `${top}%`,
                    animationDelay: `${delay}s`,
                    animationDuration: `${duration}s`,
                    opacity: 0.3
                  }}
                ></div>
              );
            })}
          </div>
        )}

        <div className="mx-auto max-w-6xl px-6 lg:px-8 text-center relative z-10">
          {/* Redesigned Header */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="mb-16"
          >
            {/* Animated Badge */}
            <motion.div
              className="inline-flex items-center gap-3 px-6 py-3 bg-gradient-to-r from-purple-500 via-indigo-500 to-blue-500 text-white rounded-full mb-8 shadow-2xl"
              whileHover={{ scale: 1.1, rotate: 3 }}
              animate={{
                boxShadow: [
                  "0 10px 30px rgba(139, 92, 246, 0.3)",
                  "0 10px 50px rgba(99, 102, 241, 0.5)",
                  "0 10px 30px rgba(139, 92, 246, 0.3)",
                ],
              }}
              transition={{ duration: 3, repeat: Infinity }}
            >
              <motion.div
                animate={{ rotate: [0, 360] }}
                transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
              >
                <GraduationCap className="w-6 h-6" />
              </motion.div>
              <span className="font-bold text-sm tracking-wider">THE KNOWLEDGE EXODUS</span>
              <motion.div
                animate={{ scale: [1, 1.3, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                <Sparkles className="w-5 h-5" />
              </motion.div>
            </motion.div>

            {/* Main Heading - Dramatic & Impactful */}
            <div className="relative inline-block">
              <h2 className="font-serif text-4xl md:text-6xl lg:text-7xl font-black mb-6">
                <span className="block text-[#1E3A8A] mb-2">When Brilliant Minds</span>
                <span className="block">
                  <span className="bg-gradient-to-r from-purple-600 via-indigo-600 to-blue-600 bg-clip-text text-transparent animate-gradient bg-[length:200%_auto]">
                    Leave Their Wisdom Behind
                  </span>
                </span>
              </h2>

              {/* Decorative Elements */}
              <motion.div
                className="absolute -top-8 -left-12 text-purple-300/40"
                animate={{
                  rotate: [0, 10, -10, 0],
                  y: [0, -10, 0],
                }}
                transition={{ duration: 4, repeat: Infinity }}
              >
                <Brain className="w-16 h-16" />
              </motion.div>
              <motion.div
                className="absolute -top-6 -right-12 text-indigo-300/40"
                animate={{
                  rotate: [0, -10, 10, 0],
                  y: [0, 10, 0],
                }}
                transition={{ duration: 3.5, repeat: Infinity }}
              >
                <Lightbulb className="w-14 h-14" />
              </motion.div>
            </div>

            {/* Subtitle with Animation */}
            <motion.p
              className="text-xl md:text-2xl text-gray-600 max-w-4xl mx-auto leading-relaxed"
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.3 }}
            >
              Every graduating batch carries away{" "}
              <span className="font-bold text-purple-600">4 years of hard-earned experience</span>
              {" "}— leaving the next generation to start from{" "}
              <span className="font-bold text-red-600 italic">zero</span>
            </motion.p>

            {/* Visual Accent */}
            <motion.div
              className="flex justify-center gap-2 mt-6"
              initial={{ opacity: 0, scale: 0 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.5 }}
            >
              {[...Array(5)].map((_, i) => (
                <motion.div
                  key={i}
                  className="w-3 h-3 rounded-full bg-gradient-to-r from-purple-500 to-indigo-500"
                  animate={{
                    scale: [1, 1.5, 1],
                    opacity: [0.5, 1, 0.5],
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                    delay: i * 0.2,
                  }}
                />
              ))}
            </motion.div>
          </motion.div>

          {/* Enhanced Timeline with 2022-2026 */}
          <div className="relative py-20">
            {/* Animated Timeline Line */}
            <div className="absolute left-1/2 top-0 bottom-0 w-1 -translate-x-1/2 overflow-hidden">
              <div className="w-full h-full bg-gradient-to-b from-red-400 via-orange-400 to-[#D4AF37] animate-gradient-y"></div>
            </div>

            {/* Gradient Glow */}
            <div className="absolute left-1/2 top-0 bottom-0 w-32 translate-x-1/2 bg-gradient-to-r from-transparent via-[#D4AF37]/20 to-transparent blur-xl"></div>

            {["2022", "2023", "2024", "2025", "2026"].map((year, idx) => {
              const isCurrentYear = year === "2026";
              const isPast = idx < 4;
              return (
                <div 
                  key={year}
                  className="relative mb-16 last:mb-0 animate-slide-in-up group"
                  style={{ animationDelay: `${idx * 150}ms` }}
                >
                  <div className="flex items-center justify-center gap-12">
                    {/* Left Side - Batch Info */}
                    <div className={`flex-1 text-right transition-all duration-500 ${isCurrentYear ? 'opacity-100' : 'opacity-70 group-hover:opacity-100'}`}>
                      <div className="inline-block">
                        <div className="text-3xl font-bold text-gray-900 mb-2">{year} Batch</div>
                        <div className="flex items-center justify-end gap-2 text-sm text-gray-600">
                          <Users className="w-4 h-4" />
                          <span>{3000 + idx * 200} students</span>
                        </div>
                        {isPast && (
                          <div className="mt-2 text-xs text-red-600 font-semibold">
                            <span className="inline-flex items-center gap-1">
                              <TrendingDown className="w-3 h-3" />
                              {(4 - idx) * 250}+ problems forgotten
                            </span>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Center Node */}
                    <div className="relative z-10 flex-shrink-0">
                      <div className={`relative w-20 h-20 rounded-2xl flex items-center justify-center shadow-2xl transition-all duration-500 group-hover:scale-125 ${
                        isCurrentYear 
                          ? 'bg-gradient-to-br from-[#D4AF37] to-[#F4D03F] ring-4 ring-[#D4AF37]/30' 
                          : 'bg-gradient-to-br from-red-500 to-red-600 ring-4 ring-red-300/30'
                      }`}>
                        <div className="absolute inset-0 rounded-2xl bg-gradient-to-t from-black/20 to-transparent"></div>
                        {isCurrentYear ? (
                          <Sparkles className="w-10 h-10 text-white relative z-10 animate-pulse" />
                        ) : (
                          <X className="w-10 h-10 text-white relative z-10" />
                        )}
                        
                        {/* Pulsing Rings for current year */}
                        {isCurrentYear && (
                          <>
                            <div className="absolute inset-0 rounded-2xl border-2 border-[#D4AF37] animate-ping-slow"></div>
                            <div className="absolute inset-0 rounded-2xl border-2 border-[#D4AF37] animate-ping-slow" style={{ animationDelay: '1s' }}></div>
                          </>
                        )}
                      </div>
                    </div>

                    {/* Right Side - Status */}
                    <div className={`flex-1 text-left transition-all duration-500 ${isCurrentYear ? 'opacity-100' : 'opacity-70 group-hover:opacity-100'}`}>
                      <div className={`inline-block px-6 py-3 rounded-xl ${
                        isCurrentYear 
                          ? 'bg-gradient-to-r from-[#D4AF37] to-[#F4D03F] text-[#1E3A8A]' 
                          : 'bg-gradient-to-r from-red-500 to-red-600 text-white'
                      } shadow-lg`}>
                        <div className="text-xl font-bold">
                          {isCurrentYear ? '✨ YOU ARE HERE' : '💔 Wisdom Lost'}
                        </div>
                        {!isCurrentYear && (
                          <div className="text-sm mt-1 opacity-90">
                            Graduated {2026 - parseInt(year)} years ago
                          </div>
                        )}
                      </div>
                      {isCurrentYear && (
                        <div className="mt-3 text-sm text-green-600 font-semibold flex items-center gap-2">
                          <CheckCircle2 className="w-4 h-4" />
                          <span>Time to break the cycle!</span>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Lost Knowledge Examples */}
                  {isPast && (
                    <div className="mt-6 mx-auto max-w-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500">
                      <div className="bg-white/80 backdrop-blur-sm rounded-xl p-4 shadow-lg border border-red-200">
                        <div className="text-xs text-gray-600 mb-2 font-semibold">Lost Knowledge:</div>
                        <div className="flex flex-wrap gap-2">
                          {[
                            '📍 Parking hacks',
                            '🏃 Event shortcuts',
                            '📚 Study spots',
                            '🍽️ Food timing',
                            '📄 Document templates',
                            '🤝 Faculty contacts'
                          ].slice(0, 4).map((item, i) => (
                            <span key={i} className="text-xs px-3 py-1 bg-red-50 text-red-700 rounded-full border border-red-200">
                              {item}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {/* The Problem Today */}
          <div className="mt-20 max-w-4xl mx-auto">
            <div className="bg-gradient-to-br from-white to-gray-50 rounded-3xl shadow-2xl border-2 border-gray-200 overflow-hidden">
              <div className="bg-gradient-to-r from-red-500 to-orange-500 p-6 text-white">
                <h3 className="text-2xl font-bold flex items-center gap-3">
                  <AlertTriangle className="w-8 h-8" />
                  Right now, juniors learn through:
                </h3>
              </div>
              <div className="p-8">
                <div className="grid md:grid-cols-2 gap-4">
                  {[
                    { icon: <TrendingDown />, text: "Trial and error (costly)", cost: "₹15K lost" },
                    { icon: <MessageCircle />, text: "Incomplete hearsay", cost: "50% accuracy" },
                    { icon: <Target />, text: "Starting from zero", cost: "200hrs wasted" },
                    { icon: <X />, text: "Repeating seniors' mistakes", cost: "Same problems" }
                  ].map((item, idx) => (
                    <div key={idx} className="group flex items-center gap-4 p-5 rounded-2xl bg-gradient-to-r from-red-50 to-orange-50 hover:from-red-100 hover:to-orange-100 transition-all duration-300 border-2 border-red-200 hover:border-red-300">
                      <div className="flex-shrink-0 w-12 h-12 rounded-xl bg-red-500 text-white flex items-center justify-center group-hover:scale-110 group-hover:rotate-6 transition-all">
                        {item.icon}
                      </div>
                      <div className="flex-1">
                        <div className="font-semibold text-gray-900">{item.text}</div>
                        <div className="text-xs text-red-600 font-bold mt-1">{item.cost}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Big Question */}
          <div className="mt-16">
            <div className="inline-block relative">
              <div className="absolute -inset-4 bg-gradient-to-r from-[#D4AF37]/20 to-[#059669]/20 blur-2xl rounded-full"></div>
              <p className="relative text-3xl md:text-4xl font-serif font-bold text-[#1E3A8A] italic px-8 py-6">
                "What if every batch left behind a
                <span className="block mt-2 bg-gradient-to-r from-[#D4AF37] to-[#059669] bg-clip-text text-transparent">
                  legacy of learned lessons?
                </span>"
              </p>
            </div>
          </div>

          {/* Stat Cards */}
          <div className="mt-16 grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            {[
              { number: "4 years", label: "Of wisdom lost", icon: <Clock /> },
              { number: "1000+", label: "Problems per batch", icon: <AlertTriangle /> },
              { number: "0", label: "Institutional memory", icon: <Brain /> }
            ].map((stat, idx) => (
              <div key={idx} className="group p-6 bg-white rounded-2xl shadow-lg border-2 border-gray-100 hover:border-[#D4AF37] hover:shadow-2xl transition-all duration-300">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-[#1E3A8A] to-[#1E40AF] text-white flex items-center justify-center mb-4 group-hover:scale-110 group-hover:rotate-6 transition-all">
                  {stat.icon}
                </div>
                <div className="text-4xl font-bold text-gray-900 mb-2">{stat.number}</div>
                <div className="text-sm text-gray-600">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Continue with remaining sections... Due to length, I'll shorten the final sections */}
      
      {/* College Selection Modal */}
      {showCollegeModal && (
        <div className="fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fade-in">
          <div className="bg-white rounded-3xl shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden animate-scale-in">
            {/* Modal Header */}
            <div className="bg-gradient-to-r from-[#1E3A8A] to-[#1E40AF] p-8 text-white">
              <div className="flex items-center justify-between mb-6">
                <h3 className="font-serif text-3xl font-bold">Select Your College</h3>
                <button
                  onClick={() => setShowCollegeModal(false)}
                  className="p-2 hover:bg-white/20 rounded-full transition-colors"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>

              {/* Search Bar */}
              <div className="relative">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search by college name or city..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-12 pr-4 py-4 rounded-xl bg-white/10 backdrop-blur-sm border-2 border-white/20 text-white placeholder-white/50 focus:border-[#D4AF37] focus:outline-none transition-colors"
                />
              </div>
            </div>

            {/* College Grid */}
            <div className="p-8 overflow-y-auto max-h-[500px]">
              {/* Add College Button */}
              <button
                onClick={() => {
                  setShowCollegeModal(false);
                  setShowAddCollegeModal(true);
                }}
                className="w-full mb-6 p-6 rounded-xl border-2 border-dashed border-[#D4AF37] hover:bg-[#D4AF37]/5 transition-all duration-300 group"
              >
                <div className="flex items-center justify-center gap-3 text-[#D4AF37]">
                  <Plus className="w-6 h-6 group-hover:rotate-90 transition-transform duration-300" />
                  <span className="text-lg font-bold">Add Your College</span>
                </div>
              </button>

              <div className="grid md:grid-cols-2 gap-4">
                {filteredColleges.map((college) => (
                  <button
                    key={college.id}
                    onClick={() => handleCollegeSelect(college.id)}
                    className="group text-left p-6 rounded-xl border-2 border-gray-100 hover:border-[#D4AF37] hover:shadow-xl transition-all duration-300 bg-white overflow-hidden"
                  >
                    <div className="flex items-start gap-4">
                      {/* College Logo - Image or Color */}
                      {college.color.startsWith('http') ? (
                        <div className="relative w-12 h-12 rounded-full flex-shrink-0 overflow-hidden border-2 border-gray-200">
                          <img 
                            src={college.color} 
                            alt={college.shortName}
                            className="w-full h-full object-cover"
                          />
                          {/* Fade overlay for better text visibility */}
                          <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent"></div>
                        </div>
                      ) : (
                        <div 
                          className="w-12 h-12 rounded-full flex-shrink-0"
                          style={{ backgroundColor: college.color }}
                        ></div>
                      )}
                      <div className="flex-1 min-w-0">
                        <h4 className="font-bold text-gray-900 mb-1 group-hover:text-[#1E3A8A] truncate">
                          {college.shortName}
                        </h4>
                        <p className="text-sm text-gray-600 mb-2">
                          {college.city}, {college.state}
                        </p>
                        <div className="flex items-center gap-2 text-xs text-gray-500">
                          <span>{college.type}</span>
                          <span>•</span>
                          <span>Est. {college.established}</span>
                        </div>
                      </div>
                      <ChevronRight className="w-5 h-5 text-gray-400 group-hover:text-[#D4AF37] group-hover:translate-x-1 transition-all" />
                    </div>
                  </button>
                ))}
              </div>

              {filteredColleges.length === 0 && (
                <div className="text-center py-12">
                  <p className="text-gray-500 mb-4">No colleges found matching your search</p>
                  <button
                    onClick={() => setSearchQuery("")}
                    className="text-[#1E3A8A] font-semibold hover:underline"
                  >
                    Clear search
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Login Modal */}
      <LoginModal 
        isOpen={showLoginModal}
        onClose={() => setShowLoginModal(false)}
        onLogin={handleLogin}
      />

      {/* Add College Modal */}
      <AnimatePresence>
        {showAddCollegeModal && (
          <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="bg-white rounded-3xl shadow-2xl w-full max-w-2xl overflow-hidden"
            >
              {/* Header */}
              <div className="bg-gradient-to-r from-[#1E3A8A] to-[#1E40AF] p-6 text-white relative">
                <button
                  onClick={() => setShowAddCollegeModal(false)}
                  className="absolute top-4 right-4 p-2 hover:bg-white/20 rounded-full transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
                <h3 className="text-2xl font-bold">Add Your College</h3>
                <p className="text-white/80 text-sm mt-1">Help us expand Campus Memory</p>
              </div>

              {/* Form */}
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  const formData = new FormData(e.currentTarget);
                  handleAddCollege({
                    name: formData.get('name'),
                    shortName: formData.get('shortName'),
                    city: formData.get('city'),
                    state: formData.get('state'),
                    type: formData.get('type'),
                    established: parseInt(formData.get('established') as string),
                    studentStrength: parseInt(formData.get('studentStrength') as string),
                    color: formData.get('color') || '#3B82F6',
                  });
                }}
                className="p-6 space-y-4 max-h-[70vh] overflow-y-auto"
              >
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">College Name *</label>
                    <input
                      type="text"
                      name="name"
                      required
                      placeholder="Full college name"
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-[#1E3A8A] focus:outline-none transition-colors"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Short Name *</label>
                    <input
                      type="text"
                      name="shortName"
                      required
                      placeholder="Abbreviated name"
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-[#1E3A8A] focus:outline-none transition-colors"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">City *</label>
                    <input
                      type="text"
                      name="city"
                      required
                      placeholder="City"
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-[#1E3A8A] focus:outline-none transition-colors"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">State *</label>
                    <input
                      type="text"
                      name="state"
                      required
                      placeholder="State"
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-[#1E3A8A] focus:outline-none transition-colors"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Type *</label>
                    <select
                      name="type"
                      required
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-[#1E3A8A] focus:outline-none transition-colors"
                    >
                      <option value="Private">Private</option>
                      <option value="State">State</option>
                      <option value="Central">Central</option>
                      <option value="IIT">IIT</option>
                      <option value="NIT">NIT</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Established *</label>
                    <input
                      type="number"
                      name="established"
                      required
                      min="1800"
                      max={new Date().getFullYear()}
                      placeholder="Year"
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-[#1E3A8A] focus:outline-none transition-colors"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Student Strength *</label>
                    <input
                      type="number"
                      name="studentStrength"
                      required
                      min="0"
                      placeholder="Approximate number"
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-[#1E3A8A] focus:outline-none transition-colors"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Color or Image URL</label>
                    <input
                      type="text"
                      name="color"
                      placeholder="#3B82F6 or https://..."
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-[#1E3A8A] focus:outline-none transition-colors"
                    />
                  </div>
                </div>

                <div className="flex gap-3 pt-4">
                  <button
                    type="button"
                    onClick={() => setShowAddCollegeModal(false)}
                    className="flex-1 px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-xl font-semibold hover:bg-gray-50 transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="flex-1 bg-gradient-to-r from-[#1E3A8A] to-[#1E40AF] text-white px-6 py-3 rounded-xl font-semibold hover:shadow-lg transition-all"
                  >
                    Add College
                  </button>
                </div>
              </form>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

      <style jsx global>{`
        @keyframes float {
          0%, 100% { transform: translate(-50%, -50%) translateY(0px); }
          50% { transform: translate(-50%, -50%) translateY(-20px); }
        }

        @keyframes float-particle {
          0% { 
            transform: translate(0, 0) scale(1);
            opacity: 0;
          }
          10% {
            opacity: 1;
          }
          90% {
            opacity: 1;
          }
          100% { 
            transform: translate(0, -100vh) scale(0.5);
            opacity: 0;
          }
        }

        @keyframes float-slow {
          0%, 100% { 
            transform: translateY(0px) translateX(0px);
          }
          25% {
            transform: translateY(-20px) translateX(10px);
          }
          50% {
            transform: translateY(-10px) translateX(-10px);
          }
          75% {
            transform: translateY(-30px) translateX(5px);
          }
        }

        @keyframes fade-in {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }

        @keyframes fade-in-up {
          from { opacity: 0; transform: translateY(40px); }
          to { opacity: 1; transform: translateY(0); }
        }

        @keyframes slide-in-left {
          from { opacity: 0; transform: translateX(-40px); }
          to { opacity: 1; transform: translateX(0); }
        }

        @keyframes slide-in-right {
          from { opacity: 0; transform: translateX(40px); }
          to { opacity: 1; transform: translateX(0); }
        }

        @keyframes scale-in {
          from { opacity: 0; transform: scale(0.9); }
          to { opacity: 1; transform: scale(1); }
        }

        @keyframes bounce-subtle {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-5px); }
        }

        @keyframes pulse-slow {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.6; }
        }

        @keyframes ping-slow {
          0% {
            transform: scale(1);
            opacity: 1;
          }
          75%, 100% {
            transform: scale(2);
            opacity: 0;
          }
        }

        @keyframes gradient-x {
          0%, 100% {
            background-position: 0% 50%;
          }
          50% {
            background-position: 100% 50%;
          }
        }

        @keyframes gradient-y {
          0%, 100% {
            background-position: 50% 0%;
          }
          50% {
            background-position: 50% 100%;
          }
        }

        @keyframes dash {
          to {
            stroke-dashoffset: -20;
          }
        }

        .animate-float-particle { animation: float-particle linear infinite; }
        .animate-float-slow { animation: float-slow ease-in-out infinite; }
        .animate-fade-in { animation: fade-in 0.8s ease-out forwards; }
        .animate-fade-in-up { animation: fade-in-up 0.8s ease-out forwards; }
        .animate-slide-in-left { animation: slide-in-left 0.8s ease-out forwards; }
        .animate-slide-in-right { animation: slide-in-right 0.8s ease-out forwards; }
        .animate-slide-in-up { animation: fade-in-up 0.8s ease-out forwards; }
        .animate-scale-in { animation: scale-in 0.3s ease-out forwards; }
        .animate-bounce-subtle { animation: bounce-subtle 2s ease-in-out infinite; }
        .animate-pulse-slow { animation: pulse-slow 3s ease-in-out infinite; }
        .animate-ping-slow { animation: ping-slow 3s cubic-bezier(0, 0, 0.2, 1) infinite; }
        .animate-gradient-x { 
          background-size: 200% auto;
          animation: gradient-x 3s ease infinite;
        }
        .animate-gradient-y { 
          background-size: auto 200%;
          animation: gradient-y 3s ease infinite;
        }
        .animate-dash { 
          stroke-dasharray: 6 6;
          animation: dash 1s linear infinite;
        }

        /* Scroll-triggered animations */
        @media (prefers-reduced-motion: no-preference) {
          [class*="animate-"] {
            animation-fill-mode: both;
          }
        }
      `}</style>

      {/* FOOTER SECTION - At the end */}
      <Footer />
    </main>
  );
}
