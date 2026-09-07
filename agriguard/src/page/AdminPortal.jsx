import React, { useState } from "react";
import {
  ShieldCheck,
  Users,
  Sprout,
  Activity,
  AlertTriangle,
  MapPin,
  Bell,
  FileText,
  User,
  LogOut,
  TrendingUp,
  CheckCircle
} from "lucide-react";

export default function AdminPortal({ admin, onLogout }) {

  const [activeSection, setActiveSection] = useState("dashboard");

  const adminData = admin || {
    name: "Agriculture Officer",
    department: "Department of Agriculture",
    district: "Nashik",
    designation: "Agricultural Extension Officer"
  };

  return (

    <div className="min-h-screen bg-slate-50">

      {/* HEADER */}

      <header className="bg-white border-b border-slate-200 sticky top-0 z-40">

        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">

          <div className="flex items-center gap-3">

            <div className="bg-slate-900 text-white p-2 rounded-xl">
              <ShieldCheck />
            </div>

            <div>

              <h1 className="font-black text-lg">
                Maha Crop Guard
              </h1>

              <p className="text-[10px] text-emerald-600 font-bold">
                Official Administration Portal
              </p>

            </div>

          </div>


          <div className="flex items-center gap-4">

            <div className="hidden sm:block text-right">

              <p className="text-xs font-bold">
                {adminData.name}
              </p>

              <p className="text-[10px] text-slate-500">
                {adminData.designation}
              </p>

            </div>

            <div className="bg-slate-100 p-2 rounded-full">
              <User className="w-5 h-5" />
            </div>

            <button
              onClick={onLogout}
              className="flex items-center gap-1 text-red-600 border border-red-200 px-3 py-2 rounded-lg text-xs font-bold"
            >

              <LogOut className="w-4 h-4" />

              Logout

            </button>

          </div>

        </div>

      </header>


      <div className="max-w-7xl mx-auto px-6 py-6">

        {/* HEADER */}

        <div className="bg-linear-to-r from-slate-900 to-emerald-900 text-white rounded-2xl p-6 mb-6">

          <p className="text-emerald-300 text-xs font-bold uppercase">
            Official Dashboard
          </p>

          <h2 className="text-2xl font-black mt-1">
            Agricultural Disease Monitoring System
          </h2>

          <p className="text-xs text-slate-300 mt-2">
            Monitor farmers, crop diseases and regional outbreaks.
          </p>

        </div>


        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">

          {/* SIDEBAR */}

          <aside className="lg:col-span-3 bg-white rounded-2xl border border-slate-200 p-3 h-fit">

            <AdminButton
              icon={<Activity />}
              text="Dashboard"
              active={activeSection === "dashboard"}
              onClick={() => setActiveSection("dashboard")}
            />

            <AdminButton
              icon={<Users />}
              text="Registered Farmers"
              active={activeSection === "farmers"}
              onClick={() => setActiveSection("farmers")}
            />

            <AdminButton
              icon={<AlertTriangle />}
              text="Disease Reports"
              active={activeSection === "diseases"}
              onClick={() => setActiveSection("diseases")}
            />

            <AdminButton
              icon={<MapPin />}
              text="Disease Map"
              active={activeSection === "map"}
              onClick={() => setActiveSection("map")}
            />

            <AdminButton
              icon={<Bell />}
              text="Alerts"
              active={activeSection === "alerts"}
              onClick={() => setActiveSection("alerts")}
            />

            <AdminButton
              icon={<User />}
              text="Admin Profile"
              active={activeSection === "profile"}
              onClick={() => setActiveSection("profile")}
            />

          </aside>


          {/* CONTENT */}

          <main className="lg:col-span-9">


            {/* DASHBOARD */}

            {activeSection === "dashboard" && (

              <div className="space-y-6">

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">

                  <AdminStat
                    icon={<Users />}
                    title="Registered Farmers"
                    value="1,248"
                  />

                  <AdminStat
                    icon={<Sprout />}
                    title="Crop Reports"
                    value="3,842"
                  />

                  <AdminStat
                    icon={<AlertTriangle />}
                    title="Active Disease Cases"
                    value="126"
                  />

                  <AdminStat
                    icon={<CheckCircle />}
                    title="Resolved Cases"
                    value="3,214"
                  />

                </div>


                {/* DISEASE ANALYTICS */}

                <div className="bg-white rounded-2xl border border-slate-200 p-6">

                  <h3 className="font-black text-lg">
                    Disease Overview
                  </h3>

                  <p className="text-xs text-slate-500 mt-1">
                    Disease reports by crop.
                  </p>


                  <div className="space-y-4 mt-6">

                    <ProgressBar
                      crop="Rice"
                      disease="Brown Spot"
                      value="72%"
                    />

                    <ProgressBar
                      crop="Cotton"
                      disease="Leaf Curl"
                      value="61%"
                    />

                    <ProgressBar
                      crop="Potato"
                      disease="Late Blight"
                      value="84%"
                    />

                    <ProgressBar
                      crop="Tomato"
                      disease="Early Blight"
                      value="68%"
                    />

                  </div>

                </div>


                {/* MAP */}

                <div className="bg-white rounded-2xl border border-slate-200 p-6">

                  <h3 className="font-black text-lg">
                    Regional Disease Monitoring
                  </h3>

                  <div className="mt-4 h-72 bg-linear-to-br from-emerald-100 via-slate-200 to-red-100 rounded-2xl relative">

                    <MapPoint
                      top="30%"
                      left="35%"
                      label="Nashik"
                    />

                    <MapPoint
                      top="50%"
                      left="55%"
                      label="Pune"
                    />

                    <MapPoint
                      top="65%"
                      left="72%"
                      label="Ahmednagar"
                    />

                  </div>

                </div>

              </div>

            )}


            {/* FARMERS */}

            {activeSection === "farmers" && (

              <div className="bg-white rounded-2xl border border-slate-200 p-6">

                <h2 className="text-xl font-black">
                  Registered Farmers
                </h2>

                <p className="text-xs text-slate-500 mt-1">
                  Farmer information and crop health activity.
                </p>


                <div className="overflow-x-auto mt-6">

                  <table className="w-full text-xs">

                    <thead>

                      <tr className="border-b text-left">

                        <th className="p-3">Farmer</th>
                        <th className="p-3">Village</th>
                        <th className="p-3">Crop</th>
                        <th className="p-3">Reports</th>
                        <th className="p-3">Status</th>

                      </tr>

                    </thead>


                    <tbody>

                      <FarmerRow
                        name="Ramesh Patil"
                        village="Nashik"
                        crop="Tomato"
                        reports="12"
                        status="Active"
                      />

                      <FarmerRow
                        name="Suresh Jadhav"
                        village="Pune"
                        crop="Potato"
                        reports="8"
                        status="Active"
                      />

                      <FarmerRow
                        name="Priya Shinde"
                        village="Ahmednagar"
                        crop="Cotton"
                        reports="15"
                        status="Active"
                      />

                      <FarmerRow
                        name="Amit Pawar"
                        village="Satara"
                        crop="Rice"
                        reports="5"
                        status="Resolved"
                      />

                    </tbody>

                  </table>

                </div>

              </div>

            )}


            {/* DISEASE REPORTS */}

            {activeSection === "diseases" && (

              <div className="bg-white rounded-2xl border border-slate-200 p-6">

                <h2 className="text-xl font-black">
                  Disease Reports
                </h2>

                <div className="grid md:grid-cols-3 gap-4 mt-6">

                  <DiseaseCard
                    disease="Late Blight"
                    crop="Potato"
                    reports="48"
                    severity="High"
                  />

                  <DiseaseCard
                    disease="Leaf Curl"
                    crop="Cotton"
                    reports="31"
                    severity="Medium"
                  />

                  <DiseaseCard
                    disease="Brown Spot"
                    crop="Rice"
                    reports="27"
                    severity="Medium"
                  />

                </div>


                <div className="mt-6">

                  <h3 className="font-bold text-sm">
                    Action Taken
                  </h3>

                  <div className="mt-3 space-y-3">

                    <ActionRow
                      farmer="Ramesh Patil"
                      disease="Late Blight"
                      action="Mancozeb recommended"
                      status="Completed"
                    />

                    <ActionRow
                      farmer="Priya Shinde"
                      disease="Leaf Curl"
                      action="Field inspection scheduled"
                      status="Pending"
                    />

                  </div>

                </div>

              </div>

            )}


            {/* MAP */}

            {activeSection === "map" && (

              <div className="bg-white rounded-2xl border border-slate-200 p-6">

                <h2 className="text-xl font-black">
                  Disease Outbreak Map
                </h2>

                <p className="text-xs text-slate-500">
                  Visualise disease concentration by region.
                </p>


                <div className="mt-5 h-112.5 bg-linear-to-br from-emerald-100 via-slate-200 to-red-100 rounded-2xl relative">

                  <MapPoint
                    top="25%"
                    left="30%"
                    label="Nashik • 42 cases"
                  />

                  <MapPoint
                    top="45%"
                    left="50%"
                    label="Pune • 27 cases"
                  />

                  <MapPoint
                    top="65%"
                    left="65%"
                    label="Ahmednagar • 31 cases"
                  />

                  <MapPoint
                    top="35%"
                    left="75%"
                    label="Aurangabad • 18 cases"
                  />

                </div>

              </div>

            )}


            {/* ALERTS */}

            {activeSection === "alerts" && (

              <div className="space-y-4">

                <h2 className="text-xl font-black">
                  Official Alerts
                </h2>

                <AdminAlert
                  title="High Disease Concentration"
                  text="Late Blight cases have increased in the monitored potato-growing region."
                />

                <AdminAlert
                  title="Weather Risk"
                  text="High humidity and rainfall may increase fungal disease probability."
                />

              </div>

            )}


            {/* PROFILE */}

            {activeSection === "profile" && (

              <div className="bg-white rounded-2xl border border-slate-200 p-6">

                <h2 className="text-xl font-black">
                  Official Profile
                </h2>

                <div className="grid md:grid-cols-2 gap-4 mt-6">

                  <Profile
                    title="Name"
                    value={adminData.name}
                  />

                  <Profile
                    title="Designation"
                    value={adminData.designation}
                  />

                  <Profile
                    title="Department"
                    value={adminData.department}
                  />

                  <Profile
                    title="District"
                    value={adminData.district}
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


function AdminButton({ icon, text, active, onClick }) {

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


function AdminStat({ icon, title, value }) {

  return (

    <div className="bg-white rounded-2xl border border-slate-200 p-4">

      <div className="text-emerald-600">

        {React.cloneElement(icon, {
          className: "w-5 h-5"
        })}

      </div>

      <p className="text-[10px] text-slate-500 mt-2">
        {title}
      </p>

      <h3 className="text-xl font-black">
        {value}
      </h3>

    </div>
  );
}


function ProgressBar({ crop, disease, value }) {

  return (

    <div>

      <div className="flex justify-between text-xs mb-1">

        <span className="font-bold">
          {crop} — {disease}
        </span>

        <span>
          {value}
        </span>

      </div>

      <div className="h-2 bg-slate-100 rounded-full overflow-hidden">

        <div
          className="h-full bg-emerald-600 rounded-full"
          style={{ width: value }}
        />

      </div>

    </div>
  );
}


function MapPoint({ top, left, label }) {

  return (

    <div
      className="absolute"
      style={{ top, left }}
    >

      <div className="w-10 h-10 bg-red-500/20 rounded-full flex items-center justify-center">

        <MapPin className="text-red-600 fill-red-500" />

      </div>

      <span className="bg-white shadow px-2 py-1 rounded text-[9px] font-bold whitespace-nowrap">
        {label}
      </span>

    </div>
  );
}


function FarmerRow({
  name,
  village,
  crop,
  reports,
  status
}) {

  return (

    <tr className="border-b">

      <td className="p-3 font-bold">
        {name}
      </td>

      <td className="p-3">
        {village}
      </td>

      <td className="p-3">
        {crop}
      </td>

      <td className="p-3">
        {reports}
      </td>

      <td className="p-3 text-emerald-700 font-bold">
        {status}
      </td>

    </tr>
  );
}


function DiseaseCard({
  disease,
  crop,
  reports,
  severity
}) {

  return (

    <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">

      <p className="text-[10px] text-slate-500">
        {crop}
      </p>

      <h3 className="font-black mt-1">
        {disease}
      </h3>

      <p className="text-sm font-bold mt-3">
        {reports} reports
      </p>

      <span className="text-[10px] text-red-600 font-bold">
        {severity} Risk
      </span>

    </div>
  );
}


function ActionRow({
  farmer,
  disease,
  action,
  status
}) {

  return (

    <div className="border border-slate-200 rounded-xl p-4 flex justify-between items-center">

      <div>

        <p className="font-bold text-xs">
          {farmer}
        </p>

        <p className="text-[10px] text-slate-500">
          {disease} • {action}
        </p>

      </div>

      <span className="text-[10px] font-bold text-emerald-700">
        {status}
      </span>

    </div>
  );
}


function AdminAlert({ title, text }) {

  return (

    <div className="bg-red-50 border border-red-200 rounded-2xl p-5">

      <div className="flex gap-3">

        <AlertTriangle className="text-red-600" />

        <div>

          <h3 className="font-bold text-sm text-red-800">
            {title}
          </h3>

          <p className="text-xs text-red-700 mt-1">
            {text}
          </p>

        </div>

      </div>

    </div>
  );
}


function Profile({ title, value }) {

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