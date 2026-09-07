import { useState, useEffect, useRef } from "react";
import AdminPortal from "./page/AdminPortal.jsx";
import FarmerPortal from "./page/FarmerPortal.jsx";
import { 
  Sprout, Camera, CloudSun, Users, Globe, HelpCircle, 
  Lock, Eye, EyeOff, User, ArrowRight, ShieldCheck, 
  MapPin, CheckCircle, Phone, Leaf, LogOut, Upload, 
  RefreshCw, AlertTriangle, Thermometer, Droplets, Sun, Bot, Send, X,
  Mail, Award, Cpu, ChevronRight, FileText, Activity, Menu, 
} from 'lucide-react';



export default function App() {
  // 1. Image Slider
  const images = ['/pic3.jpg', '/pic1.jpg', '/pic2.avif', '/pic4.jpg', '/pic5.jpg'];
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentImageIndex((prevIndex) => (prevIndex + 1) % images.length);
    }, 5000);
    return () => clearInterval(timer);
  }, [images.length]);

  // 2. Authentication States
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [role, setRole] = useState('farmer');
  const [isRegistering, setIsRegistering] = useState(false);
  const [loginId, setLoginId] = useState('');
  const [password, setPassword] = useState('');

  // 3. Registration Form States
  const [registerName, setRegisterName] = useState('');
  const [registerEmail, setRegisterEmail] = useState('');
  const [registerPhone, setRegisterPhone] = useState('');
  const [registerPassword, setRegisterPassword] = useState('');
  const [registerVillage, setRegisterVillage] = useState('');
  const [registerDistrict, setRegisterDistrict] = useState('');
  const [registerState, setRegisterState] = useState('Maharashtra');

  // 4. Navigation & Layout States
  const [showPassword, setShowPassword] = useState(false);
  const [language, setLanguage] = useState('English');
  const [currentTab, setCurrentTab] = useState('home');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // 5. Image Upload & Diagnosis States
  const [selectedImage, setSelectedImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  // 6. Chatbot States
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [chatInput, setChatInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [chatMessages, setChatMessages] = useState([
    { sender: 'bot', text: 'Namaste! I am AI Krishi Mitra. Ask me anything about crop diseases, farming, or pesticides!' }
  ]);

  // --- SEPARATE INDEPENDENT HANDLERS ---

  // Standalone Registration Handler
  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://localhost:5000/api/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          name: registerName,
          email: registerEmail,
          phone: registerPhone,
          password: registerPassword,
          village: registerVillage,
          district: registerDistrict,
          state: registerState
        })
      });

      const data = await response.json();

      if (data.success) {
        alert("Account created successfully! Please login.");
        setIsRegistering(false);

        // Clear registration form
        setRegisterName('');
        setRegisterEmail('');
        setRegisterPhone('');
        setRegisterPassword('');
        setRegisterVillage('');
        setRegisterDistrict('');
      } else {
        alert(data.message || "Registration failed.");
      }
    } catch (error) {
      console.error("Registration error:", error);
      alert("Cannot connect to backend server.");
    }
  };

  // Standalone Login Handler
  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://localhost:5000/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: loginId,
          password: password,
          role: role,
        }),
      });

      const data = await response.json();

      if (data.success) {
        console.log("Login successful:", data.user);
        localStorage.setItem("user", JSON.stringify(data.user));
        setIsLoggedIn(true);
      } else {
        alert(data.message || "Invalid credentials.");
      }
    } catch (error) {
      console.error("Login error:", error);
      alert("Cannot connect to server. Make sure backend is running.");
    }
  };

  const handleGuestLogin = () => {
    setRole('farmer');
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setCurrentTab('home');
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(URL.createObjectURL(file));
      setResult(null);
    }
  };

  const handleSimulatedDiagnosis = () => {
    if (!selectedImage) return;
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setResult({
        disease: 'Late Blight (Phytophthora)',
        confidence: 0.942,
        chemical: 'Mancozeb 75% WP',
        dosage: '2.0 - 2.5 grams per liter',
        organicOption: 'Neem Oil Spray (5ml/L) & Copper Fungicide'
      });
    }, 1500);
  };

  // Standalone API Chatbot Handler
  const handleSendChat = async () => {
    if (!chatInput.trim() || isLoading) return;

    const userMessage = chatInput.trim();

    setChatMessages((prev) => [...prev, { sender: 'user', text: userMessage }]);
    setChatInput('');
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:5000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userMessage }),
      });

      const data = await response.json();

      if (response.ok && data.reply) {
        setChatMessages((prev) => [...prev, { sender: 'bot', text: data.reply }]);
      } else {
        setChatMessages((prev) => [
          ...prev,
          { sender: 'bot', text: data.message || 'Sorry, I could not process that query.' }
        ]);
      }
    } catch (error) {
      console.error("Chat Error:", error);
      setChatMessages((prev) => [
        ...prev,
        { sender: 'bot', text: 'Unable to connect to the Krishi Mitra backend server.' }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const teamMembers = [
    { name: 'Nidhi Soni', role: 'Team Lead , AI/ML' },
    { name: 'Zaina Gangopadhyay', role: 'Weather, Risk Prediction, Recommandations' },
    { name: 'Rohini Pal', role: 'Database, Maps Integration' },
    { name: 'Sonal Kumari', role: 'Backend/API lead' },
    { name: 'Adeo Banerjee', role: 'Frontend lead: Officer/ Expert Dashboard' },
    { name: 'Irfan Chawdhury', role: 'Frontend dev: Farmer App' }
  ];

 


  return (
    <div className="min-h-screen flex flex-col font-sans bg-slate-50 text-slate-800">
      
      
      
      {/* NAVBAR */}
      {!isLoggedIn && (
      <header className="bg-white/90 backdrop-blur-md sticky top-0 z-50 border-b border-slate-100 px-6 py-3.5 flex items-center justify-between shadow-sm">
        <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setCurrentTab('home')}>
          <div className="flex items-center">

            <img
            src="/icon_mahacrop.png"
            className="h-15 w-15 object-contain"/>
            
          </div>
          <div>
            <span className="font-extrabold text-xl text-emerald-950 tracking-tight block leading-tight">Maha Crop Guard</span>
            <span className="text-[11px] text-emerald-600 font-semibold tracking-wide">AI Crop Health Companion</span>
          </div>
        </div>

        {/* NAVIGATION LINKS */}
        {!isLoggedIn && (
          <nav className="hidden md:flex items-center space-x-8 text-sm font-semibold text-slate-600">
            <button 
              onClick={() => setCurrentTab('home')} 
              className={`transition ${currentTab === 'home' ? 'text-emerald-700 font-bold border-b-2 border-emerald-600 pb-1' : 'hover:text-emerald-600'}`}
            >
              Home
            </button>

            {/* Features Dropdown */}
            <div className="relative group py-2">
              <button 
                onClick={() => setCurrentTab('features')} 
                className={`transition cursor-pointer ${currentTab === 'features' ? 'text-emerald-700 font-bold border-b-2 border-emerald-600 pb-1' : 'hover:text-emerald-600'}`}
              >
                Features
              </button>
              <div className="absolute top-full left-0 w-72 bg-white border border-slate-100 shadow-xl rounded-2xl p-4 hidden group-hover:block transition-all opacity-0 group-hover:opacity-100 z-50">
                <h4 className="text-xs font-bold text-emerald-800 uppercase tracking-wider mb-2">Prototype Capabilities</h4>
                <ul className="space-y-2 text-xs text-slate-600">
                  <li className="flex items-center space-x-2"><span className="w-1.5 h-1.5 bg-emerald-500 rounded-full"></span><span>AI Disease Detection & Confidence Score</span></li>
                  <li className="flex items-center space-x-2"><span className="w-1.5 h-1.5 bg-emerald-500 rounded-full"></span><span>Pesticide & Organic Recommendations</span></li>
                  <li className="flex items-center space-x-2"><span className="w-1.5 h-1.5 bg-emerald-500 rounded-full"></span><span>Real-time Weather & Micro-climate Alerts</span></li>
                  <li className="flex items-center space-x-2"><span className="w-1.5 h-1.5 bg-emerald-500 rounded-full"></span><span>Official Hotline & Extension Helpline</span></li>
                </ul>
              </div>
            </div>

            {/* How It Works Dropdown */}
            <div className="relative group py-2">
              <button 
                onClick={() => setCurrentTab('how')} 
                className={`transition cursor-pointer ${currentTab === 'how' ? 'text-emerald-700 font-bold border-b-2 border-emerald-600 pb-1' : 'hover:text-emerald-600'}`}
              >
                How It Works
              </button>
              <div className="absolute top-full left-1/2 -translate-x-1/2 w-72 bg-white border border-slate-100 shadow-xl rounded-2xl p-4 hidden group-hover:block transition-all opacity-0 group-hover:opacity-100 z-50">
                <h4 className="text-xs font-bold text-emerald-800 uppercase tracking-wider mb-2">System Workflow</h4>
                <ol className="space-y-2 text-xs text-slate-600">
                  <li className="flex items-start space-x-2"><span className="font-bold text-emerald-600">1.</span><span>Upload Leaf Photo or Sensor Data</span></li>
                  <li className="flex items-start space-x-2"><span className="font-bold text-emerald-600">2.</span><span>AI Model Analyzes Pathogen Markers</span></li>
                  <li className="flex items-start space-x-2"><span className="font-bold text-emerald-600">3.</span><span>Get Preventive Dosage & Risk Alert</span></li>
                </ol>
              </div>
            </div>

            {/* About Us Dropdown */}
            <div className="relative group py-2">
              <button 
                onClick={() => setCurrentTab('about')} 
                className={`transition cursor-pointer ${currentTab === 'about' ? 'text-emerald-700 font-bold border-b-2 border-emerald-600 pb-1' : 'hover:text-emerald-600'}`}
              >
                About Us
              </button>
              <div className="absolute top-full left-1/2 -translate-x-1/2 w-72 bg-white border border-slate-100 shadow-xl rounded-2xl p-4 hidden group-hover:block transition-all opacity-0 group-hover:opacity-100 z-50">
                <h4 className="text-xs font-bold text-emerald-800 uppercase tracking-wider mb-1">Team Oblivion</h4>
                <p className="text-xs text-slate-500 leading-relaxed">
                  6 CSE (IoT) 3rd year students working on SIH problem statement by Govt. of Maharashtra to prevent crop loss.
                </p>
              </div>
            </div>

            {/* Contact Dropdown */}
            <div className="relative group py-2">
              <button 
                onClick={() => setCurrentTab('contact')} 
                className={`transition cursor-pointer ${currentTab === 'contact' ? 'text-emerald-700 font-bold border-b-2 border-emerald-600 pb-1' : 'hover:text-emerald-600'}`}
              >
                Contact
              </button>
              <div className="absolute top-full right-0 w-64 bg-white border border-slate-100 shadow-xl rounded-2xl p-4 hidden group-hover:block transition-all opacity-0 group-hover:opacity-100 z-50">
                <h4 className="text-xs font-bold text-emerald-800 uppercase tracking-wider mb-2">Government Helplines</h4>
                <div className="space-y-1.5 text-xs text-slate-600">
                  <p>Kisan Call Center: 1800-180-1551</p>
                  <p>Agri Dept Maharashtra: 1800-233-4000</p>
                  <p>support@mahacropguard.in</p>
                </div>
              </div>
            </div>
          </nav>
        )}

        {/* HEADER CONTROLS */}
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-1.5 text-xs font-semibold text-slate-700 bg-slate-100 px-3 py-1.5 rounded-full border border-slate-200 cursor-pointer">
            <Globe className="w-4 h-4 text-emerald-600" />
            <span>{language}</span>
          </div>
          {isLoggedIn ? (
            <button 
              onClick={handleLogout}
              className="flex items-center space-x-1.5 text-xs font-semibold text-red-600 border border-red-200 px-3 py-1.5 rounded-full hover:bg-red-50 transition"
            >
              <LogOut className="w-3.5 h-3.5" />
              <span>Logout</span>
            </button>
          ) : (
            <button 
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden text-slate-600 p-1 rounded-lg"
            >
              <Menu className="w-6 h-6" />
            </button>
          )}
        </div>
      </header>
      )}

      {/* MOBILE MENU DROPDOWN */}
      {mobileMenuOpen && !isLoggedIn && (
        <div className="md:hidden bg-white border-b border-slate-200 px-6 py-4 space-y-3 font-semibold text-sm">
          <button onClick={() => { setCurrentTab('home'); setMobileMenuOpen(false); }} className="block w-full text-left py-1 text-slate-700">Home</button>
          <button onClick={() => { setCurrentTab('features'); setMobileMenuOpen(false); }} className="block w-full text-left py-1 text-slate-700">Features</button>
          <button onClick={() => { setCurrentTab('how'); setMobileMenuOpen(false); }} className="block w-full text-left py-1 text-slate-700">How It Works</button>
          <button onClick={() => { setCurrentTab('about'); setMobileMenuOpen(false); }} className="block w-full text-left py-1 text-slate-700">About Us</button>
          <button onClick={() => { setCurrentTab('contact'); setMobileMenuOpen(false); }} className="block w-full text-left py-1 text-slate-700">Contact</button>
        </div>
      )}

      {/* DYNAMIC CONTENT ROUTING */}
      <main className="flex-1">
        {currentTab === 'home' && !isLoggedIn && (
          <section className="relative flex-1 flex items-center py-12 px-6 lg:px-16 overflow-hidden min-h-[80vh]">
            <div className="absolute inset-0 z-0">
              {images.map((imgUrl, index) => (
                <div
                  key={imgUrl}
                  className="absolute inset-0 bg-cover bg-center transition-opacity duration-1000 ease-in-out"
                  style={{
                    backgroundImage: `linear-gradient(to right, rgba(255, 255, 255, 0.85) 0%, rgba(255, 255, 255, 0.4) 50%, rgba(0, 0, 0, 0.1) 100%), url(${imgUrl})`,
                    opacity: index === currentImageIndex ? 1 : 0
                  }}
                />
              ))}
            </div>

            <div className="relative z-10 max-w-7xl mx-auto w-full grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
              <div className="lg:col-span-7 space-y-8">
                <div className="space-y-4">
                  <h1 className="text-4xl lg:text-5xl font-black text-slate-900 leading-tight tracking-tight">
                    Smart Farming, <br />
                    <span className="text-emerald-700">Healthier Harvests</span>
                  </h1>
                  <p className="text-base text-slate-700 font-medium max-w-xl leading-relaxed">
                    Maha Crop Guard enables early detection of crop diseases to protect crop yields.
                  </p>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-2">
                  <div className="flex flex-col items-center text-center p-3 bg-white/80 backdrop-blur-md rounded-2xl border border-emerald-100 shadow-sm">
                    <div className="bg-emerald-100 text-emerald-700 p-3 rounded-full mb-2"><Camera className="w-5 h-5" /></div>
                    <h4 className="text-xs font-bold text-slate-800">AI Leaf Scan</h4>
                    <p className="text-[10px] text-slate-500 mt-1">Instant disease identification</p>
                  </div>
                  <div className="flex flex-col items-center text-center p-3 bg-white/80 backdrop-blur-md rounded-2xl border border-emerald-100 shadow-sm">
                    <div className="bg-emerald-100 text-emerald-700 p-3 rounded-full mb-2"><Sprout className="w-5 h-5" /></div>
                    <h4 className="text-xs font-bold text-slate-800">Dosage Guide</h4>
                    <p className="text-[10px] text-slate-500 mt-1">Precise remedy dosage</p>
                  </div>
                  <div className="flex flex-col items-center text-center p-3 bg-white/80 backdrop-blur-md rounded-2xl border border-emerald-100 shadow-sm">
                    <div className="bg-emerald-100 text-emerald-700 p-3 rounded-full mb-2"><CloudSun className="w-5 h-5" /></div>
                    <h4 className="text-xs font-bold text-slate-800">Weather Radar</h4>
                    <p className="text-[10px] text-slate-500 mt-1">Fungal risk alerts</p>
                  </div>
                  <div className="flex flex-col items-center text-center p-3 bg-white/80 backdrop-blur-md rounded-2xl border border-emerald-100 shadow-sm">
                    <div className="bg-emerald-100 text-emerald-700 p-3 rounded-full mb-2"><Users className="w-5 h-5" /></div>
                    <h4 className="text-xs font-bold text-slate-800">Expert Desk</h4>
                    <p className="text-[10px] text-slate-500 mt-1">Official escalation portal</p>
                  </div>
                </div>

                <div className="bg-white/90 backdrop-blur-md rounded-2xl p-4 border border-emerald-100 shadow-sm flex items-center space-x-3 max-w-lg">
                  <div className="bg-emerald-600 text-white p-2 rounded-xl"><CheckCircle className="w-5 h-5" /></div>
                  <div>
                    <h5 className="text-xs font-bold text-slate-800">Govt of Maharashtra Problem Statement Focus</h5>
                    <p className="text-[11px] text-slate-500">Preventing crop financial loss through proactive early detection.</p>
                  </div>
                </div>
              </div>

              {/* LOGIN CARD */}
              <div className="lg:col-span-5 flex justify-center">
                <div className="w-full max-w-md bg-white rounded-3xl p-8 shadow-2xl border border-slate-100">
                  <div className="text-center mb-6">
                    <div className="inline-flex items-center space-x-1 text-emerald-600 mb-1">
                      <Sprout className="w-5 h-5" />
                      <span className="text-lg font-extrabold text-slate-900">Welcome Back!</span>
                      <Sprout className="w-5 h-5" />
                    </div>
                    <p className="text-xs text-slate-500">Login to continuous crop portal</p>
                  </div>

                  <div className="mb-6">
                    <span className="block text-[11px] font-bold text-slate-400 text-center uppercase tracking-wider mb-2">Select User Type</span>
                    <div className="grid grid-cols-2 gap-3">
                      <button
                        type="button"
                        onClick={() => setRole('farmer')}
                        className={`p-3 rounded-2xl border text-left flex flex-col justify-between transition ${
                          role === 'farmer' ? 'bg-emerald-50/80 border-emerald-500 text-emerald-900 shadow-sm' : 'bg-slate-50 border-slate-200 text-slate-600'
                        }`}
                      >
                        <div className="flex items-center space-x-2 font-bold text-xs mb-1"><span></span><span>Farmer</span></div>
                        <span className="text-[10px] text-slate-500">I need crop advice</span>
                      </button>

                      <button
                        type="button"
                        onClick={() => setRole('official')}
                        className={`p-3 rounded-2xl border text-left flex flex-col justify-between transition ${
                          role === 'official' ? 'bg-emerald-50/80 border-emerald-500 text-emerald-900 shadow-sm' : 'bg-slate-50 border-slate-200 text-slate-600'
                        }`}
                      >
                        <div className="flex items-center space-x-2 font-bold text-xs mb-1"><span></span><span>Official</span></div>
                        <span className="text-[10px] text-slate-500">Agri Department</span>
                      </button>
                    </div>
              </div>
               {isRegistering ? (

  /* ================= REGISTER FORM ================= */

  <form onSubmit={handleRegister} className="space-y-4">

    <div>
      <input
        type="text"
        required
        value={registerName}
        onChange={(e) => setRegisterName(e.target.value)}
        placeholder="Full Name"
        className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-emerald-500 focus:outline-none"
      />
    </div>

    <div>
      <input
        type="email"
        required
        value={registerEmail}
        onChange={(e) => setRegisterEmail(e.target.value)}
        placeholder="Email Address"
        className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-emerald-500 focus:outline-none"
      />
    </div>

    <div>
      <input
        type="text"
        value={registerPhone}
        onChange={(e) => setRegisterPhone(e.target.value)}
        placeholder="Mobile Number"
        className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-emerald-500 focus:outline-none"
      />
    </div>

    <div>
      <input
        type="password"
        required
        value={registerPassword}
        onChange={(e) => setRegisterPassword(e.target.value)}
        placeholder="Create Password"
        className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-emerald-500 focus:outline-none"
      />
    </div>

    <div className="grid grid-cols-2 gap-3">

      <input
        type="text"
        value={registerVillage}
        onChange={(e) => setRegisterVillage(e.target.value)}
        placeholder="Village"
        className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-emerald-500 focus:outline-none"
      />

      <input
        type="text"
        value={registerDistrict}
        onChange={(e) => setRegisterDistrict(e.target.value)}
        placeholder="District"
        className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-emerald-500 focus:outline-none"
      />

    </div>

    <button
      type="submit"
      className="w-full bg-emerald-800 hover:bg-emerald-900 text-white font-bold py-3.5 rounded-xl text-xs"
    >
      Create Farmer Account
    </button>

    <button
      type="button"
      onClick={() => setIsRegistering(false)}
      className="w-full text-emerald-700 font-semibold text-xs py-2"
    >
      Already registered? Login
    </button>

  </form>

) : (

  

  <form onSubmit={handleLogin} className="space-y-4">

    {/* YOUR EXISTING LOGIN FORM GOES HERE */}

  </form>

)}
                  
                  <form onSubmit={handleLogin} className="space-y-4">
                    <div>
                      <div className="relative">
                        <User className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
                        <input
                          type="text"
                          required
                          value={loginId}
                          onChange={(e) => setLoginId(e.target.value)}
                          placeholder={role === 'farmer' ? "Mobile Number / Email" : "Official Passkey"}
                          className="w-full pl-10 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                        />
                      </div>
                    </div>

                    <div>
                      <div className="relative">
                        <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
                        <input
                          type={showPassword ? "text" : "password"}
                          required
                          value={password}
                          onChange={(e) => setPassword(e.target.value)}
                          placeholder="Password"
                          className="w-full pl-10 pr-10 py-3 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                        />
                        <button
                          type="button"
                          onClick={() => setShowPassword(!showPassword)}
                          className="absolute right-3.5 top-3.5 text-slate-400 hover:text-slate-600"
                        >
                          {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                        </button>
                      </div>
                    </div>

                    <button
                      type="submit"
                      className="w-full bg-emerald-800 hover:bg-emerald-900 text-white font-bold py-3.5 rounded-xl text-xs flex items-center justify-center space-x-2 shadow-lg transition"
                    >
                      <span>Login Workspace</span>
                      <ArrowRight className="w-4 h-4" />
                    </button>
                  </form>

                  <div className="relative my-4">
                    <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-slate-200"></div></div>
                    <div className="relative flex justify-center text-[10px] uppercase"><span className="bg-white px-2 text-slate-400">or</span></div>
                  </div>

                  <button
                    onClick={handleGuestLogin}
                    className="w-full border border-slate-200 bg-slate-50 hover:bg-slate-100 text-slate-700 font-bold py-2.5 rounded-xl text-xs flex items-center justify-center space-x-2 transition"
                  >
                    <User className="w-4 h-4 text-emerald-600" />
                    <span>Continue as Guest</span>
                  </button>

                  <button
  type="button"
  onClick={() => setIsRegistering(true)}
  className="w-full mt-3 border border-emerald-200 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 font-bold py-2.5 rounded-xl text-xs transition"
>
  New farmer? Create a new account
</button>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* PLATFORM IMPACT - LANDING PAGE ONLY */}
        {currentTab === 'home' && !isLoggedIn && (
          <section className="bg-white border-y border-slate-100 py-10 px-6">
            <div className="max-w-7xl mx-auto">
              <div className="text-center mb-8">
                <span className="inline-flex items-center gap-2 bg-emerald-50 text-emerald-700 px-4 py-1.5 rounded-full text-[11px] font-bold uppercase tracking-wider">
                  <ShieldCheck className="w-4 h-4" />
                  Platform Impact
                </span>
                <h2 className="text-2xl lg:text-3xl font-black text-slate-900 mt-3">
                  Trusted Technology for Smarter Farming
                </h2>
                <p className="text-sm text-slate-500 mt-2 max-w-2xl mx-auto">
                  Empowering farmers and agricultural officials with AI-driven crop health insights.
                </p>
              </div>

              <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="bg-emerald-50/60 border border-emerald-100 rounded-2xl p-5 text-center">
                  <Sprout className="w-6 h-6 mx-auto mb-2 text-emerald-700" />
                  <h3 className="text-2xl font-black text-emerald-800">3+</h3>
                  <p className="text-sm font-bold text-slate-800">Crops Supported</p>
                  <p className="text-[11px] text-slate-500">Rice, Wheat & Tomato</p>
                </div>

                <div className="bg-blue-50/60 border border-blue-100 rounded-2xl p-5 text-center">
                  <Activity className="w-6 h-6 mx-auto mb-2 text-blue-700" />
                  <h3 className="text-2xl font-black text-blue-800">20+</h3>
                  <p className="text-sm font-bold text-slate-800">Disease Classes</p>
                  <p className="text-[11px] text-slate-500">AI-based identification</p>
                </div>

                <div className="bg-amber-50/60 border border-amber-100 rounded-2xl p-5 text-center">
                  <Camera className="w-6 h-6 mx-auto mb-2 text-amber-700" />
                  <h3 className="text-2xl font-black text-amber-800">AI</h3>
                  <p className="text-sm font-bold text-slate-800">Powered Detection</p>
                  <p className="text-[11px] text-slate-500">Image-based crop analysis</p>
                </div>

                <div className="bg-purple-50/60 border border-purple-100 rounded-2xl p-5 text-center">
                  <Bot className="w-6 h-6 mx-auto mb-2 text-purple-700" />
                  <h3 className="text-2xl font-black text-purple-800">24×7</h3>
                  <p className="text-sm font-bold text-slate-800">Digital Assistance</p>
                  <p className="text-[11px] text-slate-500">AI-powered farming guidance</p>
                </div>
              </div>

              <div className="mt-6 flex items-center justify-center gap-2 text-[11px] text-slate-500">
                <CheckCircle className="w-4 h-4 text-emerald-500" />
                <span>Built for farmers, extension workers and agricultural departments.</span>
              </div>
            </div>
          </section>
        )}

        {/* LOGGED IN DASHBOARD */}

        {isLoggedIn && role === "farmer" && (
  <FarmerPortal
    farmer={{
      name: loginId || "Ramesh Patil",
      phone: loginId || "9876543210",
      village: "Nashik",
      district: "Nashik",
      state: "Maharashtra",
      crop: "Tomato",
      farmArea: "3.5 Acres"
    }}
    onLogout={handleLogout}
  />
)}

{isLoggedIn && role === "official" && (
  <AdminPortal
    admin={{
      name: "Agriculture Officer",
      department: "Department of Agriculture",
      district: "Nashik",
      designation: "Agricultural Extension Officer"
    }}
    onLogout={handleLogout}
  />
)}
        

           

                

                

             

        {/* FEATURES SECTION */}
        {currentTab === 'features' && (
          <section className="max-w-7xl mx-auto px-6 py-10 space-y-8">
            <div className="text-center max-w-2xl mx-auto">
              <h2 className="text-3xl font-black text-slate-900">Platform Features</h2>
              <p className="text-xs text-slate-600 mt-2">
                Designed as an integrated prototype for Smart Agriculture, FoodTech, and Rural Development.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-3">
                <div className="bg-emerald-100 text-emerald-700 p-3 rounded-xl w-fit"><Camera className="w-6 h-6" /></div>
                <h3 className="font-bold text-base text-slate-900">AI Crop Disease Identification</h3>
                <p className="text-xs text-slate-600 leading-relaxed">
                  Scans uploaded leaf images to identify fungal, bacterial, and viral infections with real-time confidence scores.
                </p>
              </div>

              <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-3">
                <div className="bg-emerald-100 text-emerald-700 p-3 rounded-xl w-fit"><Leaf className="w-6 h-6" /></div>
                <h3 className="font-bold text-base text-slate-900">Pesticide & Organic Dosage Guidelines</h3>
                <p className="text-xs text-slate-600 leading-relaxed">
                  Provides exact dosage recommendations per liter for chemical solutions alongside eco-friendly organic remedies.
                </p>
              </div>

              <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-3">
                <div className="bg-emerald-100 text-emerald-700 p-3 rounded-xl w-fit"><CloudSun className="w-6 h-6" /></div>
                <h3 className="font-bold text-base text-slate-900">Daily Weather Reports & Micro-climate Risk</h3>
                <p className="text-xs text-slate-600 leading-relaxed">
                  Monitors ambient temperature, humidity, and UV metrics to generate early warnings before disease outbreaks spread.
                </p>
              </div>

              <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-3">
                <div className="bg-emerald-100 text-emerald-700 p-3 rounded-xl w-fit"><Phone className="w-6 h-6" /></div>
                <h3 className="font-bold text-base text-slate-900">Official Agriculture Helplines</h3>
                <p className="text-xs text-slate-600 leading-relaxed">
                  Direct access to State Agri Extension officers and Kisan Call Center hotlines for escalations.
                </p>
              </div>

              <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-3">
                <div className="bg-emerald-100 text-emerald-700 p-3 rounded-xl w-fit"><Cpu className="w-6 h-6" /></div>
                <h3 className="font-bold text-base text-slate-900">IoT Sensor Integration (Prototype)</h3>
                <p className="text-xs text-slate-600 leading-relaxed">
                  Connects soil moisture and leaf wetness sensor telemetry to provide predictive disease warnings.
                </p>
              </div>

              <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-3">
                <div className="bg-emerald-100 text-emerald-700 p-3 rounded-xl w-fit"><Bot className="w-6 h-6" /></div>
                <h3 className="font-bold text-base text-slate-900">AI Krishi Mitra Assistant</h3>
                <p className="text-xs text-slate-600 leading-relaxed">
                  Multilingual AI bot guiding farmers on seasonal treatments, spray schedules, and soil care.
                </p>
              </div>
            </div>
          </section>
        )}

        {/* HOW IT WORKS SECTION */}
        {currentTab === 'how' && (
          <section className="max-w-7xl mx-auto px-6 py-10 space-y-8">
            <div className="text-center max-w-2xl mx-auto">
              <h2 className="text-3xl font-black text-slate-900">How Maha Crop Guard Works</h2>
              <p className="text-xs text-slate-600 mt-2">A 3-step workflow designed for rapid response in rural agricultural environments.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white p-6 rounded-2xl border border-slate-200 text-center space-y-3">
                <div className="w-10 h-10 bg-emerald-600 text-white font-bold rounded-full flex items-center justify-center mx-auto text-sm">1</div>
                <h3 className="font-bold text-base text-slate-900">Capture Leaf Image</h3>
                <p className="text-xs text-slate-600">Take a photo of any damaged leaf or upload telemetry data from field sensors.</p>
              </div>

              <div className="bg-white p-6 rounded-2xl border border-slate-200 text-center space-y-3">
                <div className="w-10 h-10 bg-emerald-600 text-white font-bold rounded-full flex items-center justify-center mx-auto text-sm">2</div>
                <h3 className="font-bold text-base text-slate-900">AI Neural Analysis</h3>
                <p className="text-xs text-slate-600">Deep neural models analyze pathogen patterns and compare them with local climate data.</p>
              </div>

              <div className="bg-white p-6 rounded-2xl border border-slate-200 text-center space-y-3">
                <div className="w-10 h-10 bg-emerald-600 text-white font-bold rounded-full flex items-center justify-center mx-auto text-sm">3</div>
                <h3 className="font-bold text-base text-slate-900">Actionable Prescription</h3>
                <p className="text-xs text-slate-600">Receive precise organic and chemical spray instructions to isolate the threat.</p>
              </div>
            </div>
          </section>
        )}

        {/* ABOUT US SECTION */}
        {currentTab === 'about' && (
          <section className="max-w-7xl mx-auto px-6 py-10 space-y-8">
            <div className="text-center max-w-2xl mx-auto">
              <span className="bg-emerald-100 text-emerald-800 text-[10px] font-bold px-3 py-1 rounded-full uppercase tracking-wider">SIH Prototype Development</span>
              <h2 className="text-3xl font-black text-slate-900 mt-2">Meet Team Oblivion</h2>
              <p className="text-xs text-slate-600 mt-1">6 CSE (IoT) 3rd year students committed to solving real-world agricultural problems for the Govt. of Maharashtra.</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {teamMembers.map((member, i) => (
                <div key={i} className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center space-x-4">
                  <div className="bg-emerald-100 text-emerald-800 font-bold text-sm w-12 h-12 rounded-full flex items-center justify-center shrink-0">
                    {member.name.split(' ').map(n => n[0]).join('')}
                  </div>
                  <div>
                    <h3 className="font-bold text-sm text-slate-900">{member.name}</h3>
                    <p className="text-xs text-emerald-700 font-semibold">{member.role}</p>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* CONTACT SECTION */}
        {currentTab === 'contact' && (
          <section className="max-w-4xl mx-auto px-6 py-10 space-y-6">
            <div className="text-center">
              <h2 className="text-3xl font-black text-slate-900">Contact & Support</h2>
              <p className="text-xs text-slate-600 mt-1">Get immediate agricultural assistance or escalate high-risk crop outbreaks.</p>
            </div>

            <div className="bg-white rounded-2xl border border-slate-200 p-6 space-y-4">
              <div className="flex items-center space-x-3 text-slate-700">
                <Phone className="w-5 h-5 text-emerald-600" />
                <span className="text-xs font-semibold">Kisan Call Center: 1800-180-1551 (Toll Free)</span>
              </div>
              <div className="flex items-center space-x-3 text-slate-700">
                <Phone className="w-5 h-5 text-emerald-600" />
                <span className="text-xs font-semibold">Agri Dept Maharashtra Hotline: 1800-233-4000</span>
              </div>
              <div className="flex items-center space-x-3 text-slate-700">
                <Mail className="w-5 h-5 text-emerald-600" />
                <span className="text-xs font-semibold">Support Email: support@mahacropguard.in</span>
              </div>
            </div>
          </section>
        )}
      </main>



      {/* FLOATING AI CHATBOT */}



      <div className="fixed bottom-6 right-6 z-50">
        {!isChatOpen ? (
          <button
            onClick={() => setIsChatOpen(true)}
            className="bg-emerald-700 hover:bg-emerald-800 text-white p-4 rounded-full shadow-2xl flex items-center space-x-2 transition"
          >
            <Bot className="w-6 h-6" />
            <span className="text-xs font-bold pr-1">Ask AI Krishi Mitra</span>
          </button>
        ) : (
          <div className="bg-white rounded-2xl shadow-2xl border border-slate-200 w-80 sm:w-96 flex flex-col h-[420px] overflow-hidden">
            <div className="bg-emerald-800 text-white p-4 rounded-t-2xl flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Bot className="w-5 h-5" />
                <div>
                  <h4 className="text-xs font-bold">AI Krishi Mitra</h4>
                  <span className="text-[10px] text-emerald-200">Online | Ready to Help</span>
                </div>
              </div>
              <button onClick={() => setIsChatOpen(false)} className="text-emerald-200 hover:text-white"><X className="w-5 h-5" /></button>
            </div>

            <div className="flex-1 p-4 overflow-y-auto space-y-3 text-xs bg-slate-50">
              {chatMessages.map((msg, i) => (
                <div key={i} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`p-3 rounded-2xl max-w-[80%] ${msg.sender === 'user' ? 'bg-emerald-700 text-white rounded-br-none' : 'bg-white text-slate-800 border border-slate-200 rounded-bl-none shadow-sm'}`}>
                    {msg.text}
                  </div>
                </div>
              ))}

                {isLoading && (
    <div className="flex justify-start">
      <div className="p-3 rounded-2xl max-w-[80%] bg-white text-slate-500 border border-slate-200 rounded-bl-none shadow-sm italic">
        Krishi Mitra is thinking...
      </div>
    </div>
  )}

            </div>

            

            <div className="p-3 border-t border-slate-200 bg-white rounded-b-2xl flex items-center space-x-2">
              <input
                type="text"
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSendChat()}
                placeholder="Ask about crops or pesticides..."
                className="flex-1 text-xs bg-slate-100 border border-slate-200 rounded-xl px-3 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
              <button onClick={handleSendChat} className="bg-emerald-700 hover:bg-emerald-800 text-white p-2 rounded-xl">
                <Send className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}
      </div>

      {/* UPDATED GREENISH FOOTER */}
      <footer className="bg-gradient-to-r from-emerald-900 via-emerald-950 to-teal-950 border-t border-emerald-800/50 py-8 px-6 text-center text-xs text-emerald-200/80 shadow-inner">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <Sprout className="w-5 h-5 text-emerald-400" />
            <span className="font-bold text-white text-sm">Maha Crop Guard</span>
          </div>
          <p>© 2026 Maha Crop Guard | Developed by Team Oblivion.</p>
          <div className="flex space-x-4 text-[11px] text-emerald-300">
            <span className="hover:text-white cursor-pointer transition">Privacy Policy</span>
            <span>•</span>
            <span className="hover:text-white cursor-pointer transition">Terms of Service</span>
          </div>
        </div>
      </footer>

    </div>
  );
}