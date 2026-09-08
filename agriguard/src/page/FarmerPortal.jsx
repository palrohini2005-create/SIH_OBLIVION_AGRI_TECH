import React, { useState, useEffect } from "react";
import {
  Sprout,
  Camera,
  MapPin,
  Bell,
  History,
  User,
  CloudSun,
  Thermometer,
  Droplets,
  AlertTriangle,
  CheckCircle,
  Upload,
  LogOut,
  Leaf,
  Pill,
  Activity,
  X
} from "lucide-react";

export default function FarmerPortal({ farmer, onLogout }) {

  const [activeSection, setActiveSection] = useState("dashboard");
  const [selectedImage, setSelectedImage] = useState(null);
  const [diagnosis, setDiagnosis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [weather, setWeather] = useState(null);

  // Crop Alerts
  const [cropAlerts, setCropAlerts] = useState(null);
  const [alertsLoading, setAlertsLoading] = useState(true);
  const [alertsError, setAlertsError] = useState(null);


  useEffect(() => {
    fetch("http://localhost:5000/api/weather")
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setWeather(data);
        }
      })
      .catch((error) => {
        console.error("Weather error:", error);
      });
  }, []);


  const farmerData = farmer || {
    name: "Ramesh Patil",
    phone: "9876543210",
    village: "Nashik",
    district: "Nashik",
    state: "Maharashtra",
    crop: "Tomato",
    farmArea: "3.5 Acres"
  };


  // Fetch crop disease alerts from our FastAPI backend
  useEffect(() => {

    const crop = farmerData.crop || "Tomato";

    // Prototype location: Nashik
    const latitude = 20.0059;
    const longitude = 73.7897;

    setAlertsLoading(true);

    fetch(
      `http://127.0.0.1:8000/crop-alerts?crop=${encodeURIComponent(
        crop
      )}&latitude=${latitude}&longitude=${longitude}&farmer_name=${encodeURIComponent(
        farmerData.name
      )}&phone_number=${encodeURIComponent(farmerData.phone)}`
    )
      .then((res) => {

        if (!res.ok) {
          throw new Error("Failed to fetch crop alerts");
        }

        return res.json();
      })
      .then((data) => {

        setCropAlerts(data);
        setAlertsError(null);

      })
      .catch((error) => {

        console.error("Crop alerts error:", error);
        setAlertsError("Unable to load crop alerts.");

      })
      .finally(() => {

        setAlertsLoading(false);

      });

  }, [farmerData.crop, farmerData.name, farmerData.phone]);


  const handleImageUpload = (e) => {

    const file = e.target.files[0];

    if (file) {
      setSelectedImage(URL.createObjectURL(file));
      setDiagnosis(null);
    }

  };


  const runDiagnosis = () => {

    if (!selectedImage) return;

    setLoading(true);

    setTimeout(() => {

      setLoading(false);

      setDiagnosis({
        disease: "Late Blight",
        confidence: 94,
        severity: "High",
        pesticide: "Mancozeb 75% WP",
        dosage: "2–2.5 g/L",
        organic: "Neem Oil 5 ml/L",
        prevention:
          "Avoid overhead irrigation and maintain proper spacing between plants."
      });

    }, 1800);

  };


  return (

    <div className="min-h-screen bg-slate-50">

      {/* TOP NAVBAR */}

      <header className="bg-white border-b border-slate-200 sticky top-0 z-40">

        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">

          <div className="flex items-center gap-3">

            <div className="bg-emerald-700 p-2 rounded-xl text-white">
              <Sprout />
            </div>

            <div>

              <h1 className="font-black text-lg text-emerald-950">
                Maha Crop Guard
              </h1>

              <p className="text-[10px] text-emerald-600 font-semibold">
                Farmer Portal
              </p>

            </div>

          </div>


          <div className="flex items-center gap-4">

            <div className="hidden sm:block text-right">

              <p className="text-xs font-bold text-slate-800">
                {farmerData.name}
              </p>

              <p className="text-[10px] text-slate-500">
                {farmerData.village}, {farmerData.district}
              </p>

            </div>


            <div className="bg-emerald-100 text-emerald-700 p-2 rounded-full">
              <User className="w-5 h-5" />
            </div>


            <button
              onClick={onLogout}
              className="text-red-600 border border-red-200 px-3 py-2 rounded-lg text-xs font-bold flex items-center gap-1"
            >

              <LogOut className="w-4 h-4" />

              Logout

            </button>

          </div>

        </div>

      </header>


      <div className="max-w-7xl mx-auto px-6 py-6">

        {/* WELCOME */}

        <div className="bg-linear-to-r from-emerald-800 to-teal-700 rounded-2xl p-6 text-white mb-6">

          <p className="text-emerald-200 text-xs font-semibold">
            WELCOME BACK
          </p>

          <h2 className="text-2xl font-black mt-1">
            Namaste, {farmerData.name} 👋
          </h2>

          <p className="text-sm text-emerald-100 mt-2">
            Here is your crop health overview.
          </p>

        </div>


        {/* SIDEBAR + CONTENT */}

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">


          {/* SIDEBAR */}

          <aside className="lg:col-span-3 bg-white rounded-2xl border border-slate-200 p-3 h-fit">

            <PortalButton
              icon={<Activity />}
              text="Dashboard"
              active={activeSection === "dashboard"}
              onClick={() => setActiveSection("dashboard")}
            />

            <PortalButton
              icon={<Camera />}
              text="Crop Disease Scan"
              active={activeSection === "scan"}
              onClick={() => setActiveSection("scan")}
            />

            <PortalButton
              icon={<MapPin />}
              text="Disease Map"
              active={activeSection === "map"}
              onClick={() => setActiveSection("map")}
            />

            <PortalButton
              icon={<Bell />}
              text="Alerts"
              active={activeSection === "alerts"}
              onClick={() => setActiveSection("alerts")}
            />

            <PortalButton
              icon={<History />}
              text="Scan History"
              active={activeSection === "history"}
              onClick={() => setActiveSection("history")}
            />

            <PortalButton
              icon={<User />}
              text="My Profile"
              active={activeSection === "profile"}
              onClick={() => setActiveSection("profile")}
            />

          </aside>


          {/* MAIN CONTENT */}

          <main className="lg:col-span-9">


            {/* DASHBOARD */}

            {activeSection === "dashboard" && (

              <div className="space-y-6">


                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">

                  <StatCard
                    title="Crop"
                    value={farmerData.crop}
                    icon={<Leaf />}
                  />

                  <StatCard
                    title="Farm Area"
                    value={farmerData.farmArea}
                    icon={<Sprout />}
                  />

                  <StatCard
                    title="Scans"
                    value="12"
                    icon={<Camera />}
                  />

                  <StatCard
                    title="Active Alerts"
                    value={
                      cropAlerts
                        ? cropAlerts.alerts.filter(
                            (alert) =>
                              alert.alert_severity === "HIGH" ||
                              alert.alert_severity === "CRITICAL"
                          ).length
                        : "..."
                    }
                    icon={<Bell />}
                  />

                </div>


                {/* WEATHER */}

                <div className="bg-white rounded-2xl border border-slate-200 p-5">

                  <div className="flex justify-between items-center">

                    <div>

                      <h3 className="font-bold text-lg">
                        Today's Weather
                      </h3>

                      <p className="text-xs text-slate-500">
                        {farmerData.district}, Maharashtra
                      </p>

                    </div>

                    <CloudSun className="text-amber-500" />

                  </div>


                  <div className="grid grid-cols-3 gap-4 mt-5">

                    <WeatherItem
                      icon={<Thermometer />}
                      title="Temperature"
                      value={
                        weather
                          ? `${weather.temperature}°C`
                          : "Loading..."
                      }
                    />

                    <WeatherItem
                      icon={<Droplets />}
                      title="Humidity"
                      value={
                        weather
                          ? `${weather.humidity}%`
                          : "Loading..."
                      }
                    />

                    <WeatherItem
                      icon={<CloudSun />}
                      title="Rain Risk"
                      value={
                        weather
                          ? `${weather.rain_probability}%`
                          : "Loading..."
                      }
                    />

                  </div>

                </div>


                {/* REAL ALERT SUMMARY */}

                <div className="bg-red-50 border border-red-200 rounded-2xl p-5">

                  <div className="flex gap-3">

                    <AlertTriangle className="text-red-600" />

                    <div className="flex-1">

                      <h3 className="font-bold text-red-800">
                        Disease Risk Alert
                      </h3>

                      {alertsLoading ? (

                        <p className="text-xs text-red-700 mt-1">
                          Checking disease risks for your crop...
                        </p>

                      ) : alertsError ? (

                        <p className="text-xs text-red-700 mt-1">
                          {alertsError}
                        </p>

                      ) : cropAlerts && cropAlerts.alerts.length > 0 ? (

                        <div className="mt-2 space-y-1">

                          {cropAlerts.alerts
                            .filter(
                              (alert) =>
                                alert.alert_severity === "HIGH" ||
                                alert.alert_severity === "CRITICAL"
                            )
                            .map((alert) => (

                              <p
                                key={alert.disease}
                                className="text-xs text-red-700"
                              >
                                <strong>
                                  {formatDiseaseName(alert.disease)}
                                </strong>
                                {" — "}
                                {alert.risk_score}% risk
                              </p>

                            ))}

                        </div>

                      ) : (

                        <p className="text-xs text-red-700 mt-1">
                          No significant disease risk detected.
                        </p>

                      )}

                    </div>

                  </div>

                </div>


                {/* QUICK ACTION */}

                <div className="bg-white rounded-2xl border border-slate-200 p-5">

                  <h3 className="font-bold text-lg">
                    Quick Crop Check
                  </h3>

                  <p className="text-xs text-slate-500 mt-1">
                    Upload a crop image to check for possible diseases.
                  </p>

                  <button
                    onClick={() => setActiveSection("scan")}
                    className="mt-4 bg-emerald-700 text-white px-5 py-3 rounded-xl text-xs font-bold"
                  >
                    Scan My Crop
                  </button>

                </div>

              </div>

            )}


            {/* SCAN */}

            {activeSection === "scan" && (

              <div className="bg-white rounded-2xl border border-slate-200 p-6">

                <h2 className="text-xl font-black">
                  AI Crop Disease Detection
                </h2>

                <p className="text-xs text-slate-500 mt-1">
                  Upload a clear image of your crop leaf.
                </p>


                <div className="mt-6 border-2 border-dashed border-emerald-300 rounded-2xl bg-emerald-50 p-8 text-center">

                  {selectedImage ? (

                    <img
                      src={selectedImage}
                      className="max-h-64 mx-auto rounded-xl mb-5"
                      alt="Crop"
                    />

                  ) : (

                    <div className="bg-emerald-100 text-emerald-700 w-16 h-16 mx-auto rounded-full flex items-center justify-center">
                      <Upload className="w-8 h-8" />
                    </div>

                  )}


                  <input
                    id="cropUpload"
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    className="hidden"
                  />


                  <label
                    htmlFor="cropUpload"
                    className="inline-block mt-4 bg-emerald-700 text-white px-5 py-3 rounded-xl text-xs font-bold cursor-pointer"
                  >

                    {selectedImage
                      ? "Change Image"
                      : "Upload Crop Image"}

                  </label>

                </div>


                <button
                  onClick={runDiagnosis}
                  disabled={!selectedImage || loading}
                  className="w-full mt-5 bg-slate-900 text-white py-3 rounded-xl text-xs font-bold disabled:opacity-40"
                >

                  {loading
                    ? "AI Analyzing..."
                    : "Run AI Disease Detection"}

                </button>


                {/* RESULT */}

                {diagnosis && (

                  <div className="mt-6 border border-red-200 bg-red-50 rounded-2xl p-5">

                    <div className="flex justify-between">

                      <div>

                        <p className="text-[10px] font-bold uppercase text-red-500">
                          Detected Disease
                        </p>

                        <h3 className="text-xl font-black text-red-800">
                          {diagnosis.disease}
                        </h3>

                      </div>


                      <div className="text-right">

                        <p className="text-2xl font-black text-emerald-700">
                          {diagnosis.confidence}%
                        </p>

                        <p className="text-[10px]">
                          Confidence
                        </p>

                      </div>

                    </div>


                    <div className="grid md:grid-cols-2 gap-4 mt-5">

                      <Recommendation
                        icon={<Pill />}
                        title="Chemical Recommendation"
                        value={diagnosis.pesticide}
                      />

                      <Recommendation
                        icon={<Activity />}
                        title="Dosage"
                        value={diagnosis.dosage}
                      />

                      <Recommendation
                        icon={<Leaf />}
                        title="Organic Alternative"
                        value={diagnosis.organic}
                      />

                      <Recommendation
                        icon={<CheckCircle />}
                        title="Prevention"
                        value={diagnosis.prevention}
                      />

                    </div>

                  </div>

                )}

              </div>

            )}


            {/* MAP */}

            {activeSection === "map" && (

              <div className="bg-white rounded-2xl border border-slate-200 p-6">

                <h2 className="text-xl font-black">
                  Regional Disease Map
                </h2>

                <p className="text-xs text-slate-500 mt-1">
                  Disease reports around your farming area.
                </p>


                <div className="mt-5 h-100 bg-slate-200 rounded-2xl relative overflow-hidden">

                  <div className="absolute inset-0 bg-linear-to-br from-emerald-100 via-slate-200 to-blue-100" />


                  <MapMarker
                    top="35%"
                    left="45%"
                    disease="Late Blight"
                  />

                  <MapMarker
                    top="55%"
                    left="65%"
                    disease="Leaf Spot"
                  />

                  <MapMarker
                    top="25%"
                    left="70%"
                    disease="Early Blight"
                  />


                  <div className="absolute bottom-4 left-4 bg-white rounded-xl p-3 shadow text-xs">

                    <p className="font-bold">
                      Your Location
                    </p>

                    <p className="text-slate-500">
                      {farmerData.village}
                    </p>

                  </div>

                </div>

              </div>

            )}


            {/* REAL ALERTS */}

            {activeSection === "alerts" && (

              <div className="space-y-4">

                <div className="flex justify-between items-center">

                  <div>

                    <h2 className="text-xl font-black">
                      Alerts & Notifications
                    </h2>

                    <p className="text-xs text-slate-500 mt-1">
                      Disease risks detected for your {farmerData.crop}.
                    </p>

                  </div>

                  {cropAlerts && (

                    <div className="text-right">

                      <p className="text-[10px] text-slate-500">
                        Total Alerts
                      </p>

                      <p className="font-black text-lg">
                        {cropAlerts.alerts.length}
                      </p>

                    </div>

                  )}

                </div>


                {alertsLoading && (

                  <div className="bg-white border border-slate-200 rounded-2xl p-6 text-center">

                    <p className="text-sm font-bold text-slate-600">
                      Checking crop disease risks...
                    </p>

                    <p className="text-xs text-slate-400 mt-1">
                      Please wait while weather conditions are analyzed.
                    </p>

                  </div>

                )}


                {alertsError && !alertsLoading && (

                  <div className="bg-red-50 border border-red-200 rounded-2xl p-5">

                    <p className="text-sm font-bold text-red-800">
                      Unable to load alerts
                    </p>

                    <p className="text-xs text-red-700 mt-1">
                      {alertsError}
                    </p>

                  </div>

                )}


                {cropAlerts &&
                  cropAlerts.alerts.map((alert) => (

                    <DynamicAlertCard
                      key={alert.disease}
                      alert={alert}
                    />

                  ))}


                {cropAlerts &&
                  cropAlerts.alerts.length === 0 &&
                  !alertsLoading && (

                    <div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-6">

                      <div className="flex gap-3">

                        <CheckCircle className="text-emerald-600" />

                        <div>

                          <h3 className="font-bold text-emerald-800">
                            No Disease Alerts
                          </h3>

                          <p className="text-xs text-emerald-700 mt-1">
                            No significant disease risk was detected for your crop.
                          </p>

                        </div>

                      </div>

                    </div>

                  )}

              </div>

            )}


            {/* HISTORY */}

            {activeSection === "history" && (

              <div className="bg-white rounded-2xl border border-slate-200 p-6">

                <h2 className="text-xl font-black mb-5">
                  Crop Scan History
                </h2>


                <div className="overflow-x-auto">

                  <table className="w-full text-xs">

                    <thead>

                      <tr className="border-b text-left">

                        <th className="p-3">Date</th>
                        <th className="p-3">Crop</th>
                        <th className="p-3">Disease</th>
                        <th className="p-3">Confidence</th>
                        <th className="p-3">Status</th>

                      </tr>

                    </thead>


                    <tbody>

                      <tr className="border-b">

                        <td className="p-3">06 Sep 2026</td>
                        <td className="p-3">Tomato</td>
                        <td className="p-3 font-bold">Late Blight</td>
                        <td className="p-3">94%</td>

                        <td className="p-3 text-emerald-700 font-bold">
                          Treated
                        </td>

                      </tr>


                      <tr className="border-b">

                        <td className="p-3">28 Aug 2026</td>
                        <td className="p-3">Tomato</td>
                        <td className="p-3">Leaf Spot</td>
                        <td className="p-3">89%</td>

                        <td className="p-3 text-emerald-700 font-bold">
                          Resolved
                        </td>

                      </tr>

                    </tbody>

                  </table>

                </div>

              </div>

            )}


            {/* PROFILE */}

            {activeSection === "profile" && (

              <div className="bg-white rounded-2xl border border-slate-200 p-6">

                <h2 className="text-xl font-black">
                  Farmer Profile
                </h2>


                <div className="grid md:grid-cols-2 gap-4 mt-6">

                  <ProfileItem
                    title="Name"
                    value={farmerData.name}
                  />

                  <ProfileItem
                    title="Mobile"
                    value={farmerData.phone}
                  />

                  <ProfileItem
                    title="Village"
                    value={farmerData.village}
                  />

                  <ProfileItem
                    title="District"
                    value={farmerData.district}
                  />

                  <ProfileItem
                    title="State"
                    value={farmerData.state}
                  />

                  <ProfileItem
                    title="Crop"
                    value={farmerData.crop}
                  />

                  <ProfileItem
                    title="Farm Area"
                    value={farmerData.farmArea}
                  />

                </div>

              </div>

            )}

          </main>

        </div>

      </div>

    </div>

  );
}


/* COMPONENTS */


function PortalButton({ icon, text, active, onClick }) {

  return (

    <button
      onClick={onClick}
      className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-xs font-bold mb-1 ${
        active
          ? "bg-emerald-100 text-emerald-800"
          : "text-slate-600 hover:bg-slate-50"
      }`}
    >

      {React.cloneElement(icon, {
        className: "w-4 h-4"
      })}

      {text}

    </button>

  );
}


function StatCard({ title, value, icon }) {

  return (

    <div className="bg-white rounded-2xl border border-slate-200 p-4">

      <div className="text-emerald-600 mb-2">

        {React.cloneElement(icon, {
          className: "w-5 h-5"
        })}

      </div>

      <p className="text-[10px] text-slate-500">
        {title}
      </p>

      <h3 className="font-black text-lg">
        {value}
      </h3>

    </div>

  );
}


function WeatherItem({ icon, title, value }) {

  return (

    <div className="bg-slate-50 rounded-xl p-4">

      <div className="text-emerald-600">

        {React.cloneElement(icon, {
          className: "w-5 h-5"
        })}

      </div>

      <p className="text-[10px] text-slate-500 mt-2">
        {title}
      </p>

      <p className="font-black">
        {value}
      </p>

    </div>

  );
}


function Recommendation({ icon, title, value }) {

  return (

    <div className="bg-white rounded-xl p-4 border border-slate-200">

      <div className="flex gap-2 text-emerald-700">

        {React.cloneElement(icon, {
          className: "w-4 h-4"
        })}

        <p className="font-bold text-xs">
          {title}
        </p>

      </div>

      <p className="text-xs text-slate-600 mt-2">
        {value}
      </p>

    </div>

  );
}


function MapMarker({ top, left, disease }) {

  return (

    <div
      className="absolute"
      style={{ top, left }}
    >

      <div className="w-10 h-10 bg-red-500/20 rounded-full flex items-center justify-center animate-pulse">

        <MapPin className="text-red-600 fill-red-500" />

      </div>

      <div className="bg-white shadow rounded-lg px-2 py-1 text-[9px] font-bold whitespace-nowrap">
        {disease}
      </div>

    </div>

  );
}


/* Convert backend disease ID into readable name */

function formatDiseaseName(disease) {

  return disease
    .replace(/_/g, " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());

}


/* Dynamic Alert Card */

function DynamicAlertCard({ alert }) {

  const severity = alert.alert_severity;

  const styles = {

    CRITICAL:
      "bg-red-100 border-red-300 text-red-900",

    HIGH:
      "bg-red-50 border-red-200 text-red-800",

    MEDIUM:
      "bg-amber-50 border-amber-200 text-amber-800",

    LOW:
      "bg-emerald-50 border-emerald-200 text-emerald-800"

  };


  const iconStyles = {

    CRITICAL: "text-red-700",

    HIGH: "text-red-600",

    MEDIUM: "text-amber-600",

    LOW: "text-emerald-600"

  };


  return (

    <div
      className={`p-5 rounded-2xl border ${
        styles[severity] || styles.LOW
      }`}
    >

      <div className="flex gap-3">

        <Bell
          className={`w-5 h-5 ${
            iconStyles[severity] || iconStyles.LOW
          }`}
        />


        <div className="flex-1">

          <div className="flex justify-between items-start gap-3">

            <div>

              <p className="text-[10px] font-bold uppercase opacity-70">
                {severity} Risk
              </p>

              <h3 className="font-black text-base">
                {formatDiseaseName(alert.disease)}
              </h3>

            </div>


            <div className="text-right">

              <p className="text-xl font-black">
                {alert.risk_score}
              </p>

              <p className="text-[9px] opacity-70">
                Risk Score
              </p>

            </div>

          </div>


          <p className="text-xs mt-2">
            {alert.message}
          </p>


          {alert.trend && (

            <p className="text-[10px] font-bold mt-2">
              Forecast trend: {alert.trend}
            </p>

          )}


          {alert.forecast_time && (

            <p className="text-[10px] mt-1 opacity-70">
              Peak forecast: {alert.forecast_time}
            </p>

          )}


          {alert.factors && alert.factors.length > 0 && (

            <div className="mt-3">

              <p className="text-[10px] font-bold uppercase opacity-70">
                Risk Factors
              </p>

              <ul className="mt-1 space-y-1">

                {alert.factors.map((factor, index) => (

                  <li
                    key={index}
                    className="text-[10px]"
                  >
                    • {factor}
                  </li>

                ))}

              </ul>

            </div>

          )}

        </div>

      </div>

    </div>

  );

}


function ProfileItem({ title, value }) {

  return (

    <div className="bg-slate-50 rounded-xl p-4">

      <p className="text-[10px] text-slate-500">
        {title}
      </p>

      <p className="font-bold text-sm mt-1">
        {value}
      </p>

    </div>

  );

}


                 
