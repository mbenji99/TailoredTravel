import React from "react";
import bgImage from "../assets/bg-image.jpg";

function Hero({ showContent = true }) {
  return (
    <section
      className={`relative w-full ${
        showContent ? "h-screen" : "h-[35vh]"
      } bg-fixed bg-cover bg-center bg-no-repeat flex items-center justify-center`}
      style={{ backgroundImage: `url(${bgImage})`, transform: "translateZ(0)" }} // Fix GPU layering issue on some devices
    >
      {showContent && (
        <div className="bg-black/70 backdrop-blur-sm text-white px-8 py-10 rounded-2xl text-center max-w-2xl shadow-lg">
          <h1 className="text-4xl md:text-6xl font-bold text-yellow-300 mb-4 drop-shadow-lg">
            Discover Tailored Travels
          </h1>
          <p className="text-lg md:text-xl text-white/90">
            Personalized travel planning made simple.
          </p>

          {/* CTA Button */}
          <a
            href="#welcome"
            className="mt-6 inline-block px-8 py-3 bg-blue-300 text-black text-lg font-semibold rounded-xl shadow-md hover:bg-yellow-600 transition-all duration-300"
          >
            Try Tailored Travels →
          </a>
        </div>
      )}
    </section>
  );
}

export default Hero;
