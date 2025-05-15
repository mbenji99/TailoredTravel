import React from "react";
import logo from "../assets/logo.png";
import InteractionSequence from "./InteractionSequence";

function Welcome() {
  return (
    <section className="bg-white py-20 px-6 flex flex-col items-center justify-center" id="welcome">
      <div className="max-w-6xl mx-auto text-center">

        {/* Logo and Title Section */}
        <div className="flex items-center justify-center mb-6">
          <img
            src={logo}
            alt="Tailored Travels Logo"
            className="w-[150px] h-[150px] mr-3"
          />
          <h2 className="text-7xl font-bold text-yellow-500">
            Welcome to Tailored Travels
          </h2>
        </div>

        {/* Description */}
        <p className="text-2xl font-bold text-black-700 mb-8">
          Planning a trip shouldn't feel like solving a puzzle. Tailored Travels uses AI to make it easy, personal, and fun — crafting smarter, stress-free journeys tailored just for you.
        </p>

        {/* Cards Section */}
        <div className="flex flex-col gap-8 text-left">

          {/* The Problem Card */}
          <div className="bg-gray-50 p-6 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-105">
            <h3 className="text-3xl font-bold text-black-800 mb-2">The Problem We Aim to Address:</h3>
            <p className="text-gray-800 text-xl">
              With too many choices and too little guidance, planning a trip often becomes overwhelming. Generic platforms don’t understand your unique needs, causing decision fatigue and lackluster experiences.
            </p>
          </div>

          {/* Our Solution Card */}
          <div className="bg-gray-50 p-6 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-105">
            <h3 className="text-3xl font-bold text-black-800 mb-2">Our Solution:</h3>
            <p className="text-gray-800 text-xl">
              Tailored Travels delivers curated travel plans powered by AI and real-world data. It understands your preferences, adapts with your feedback, and offers dynamic suggestions for destinations, stays, and activities — all in one place.
            </p>
          </div>

          {/* Why It Matters Card */}
          <div className="bg-gray-50 p-6 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-105">
            <h3 className="text-3xl font-bold text-black-800 mb-2">Why It Matters:</h3>
            <p className="text-grey-800  text-xl">
              Most apps stop at suggestions. Tailored Travels learns, adapts, and generalizes intelligently even from limited data, offering highly relevant, contextual results in real-time. It's scalable, intelligent, and truly personal — not just a CRUD tool.
            </p>
          </div>
        </div>
      </div>

      {/* Include the Interaction Sequence Component */}
      <InteractionSequence />
    </section>
  );
}

export default Welcome;
