// components/InteractionSequence.jsx

import React from "react";
import { motion } from "framer-motion";
import { FaDollarSign, FaLightbulb, FaMapMarkedAlt } from "react-icons/fa"; 

function InteractionSequence() {
  return (
    <section className="bg-white py-20 px-6 flex flex-col items-center" id="interaction-sequence">
      <h2 className="text-2xl font-bold text-yellow-500 mb-10">How It Works</h2>

      {/* Steps Container */}
      <div className="flex flex-col md:flex-row items-center justify-around gap-12 max-w-6xl mx-auto">
        
        {/* Step 1 */}
        <motion.div
          className="flex flex-col items-center text-center"
          initial={{ opacity: 0, y: 50 }} 
          whileInView={{ opacity: 1, y: 0 }} 
          transition={{ type: "spring", stiffness: 100, damping: 25, delay: 0.2 }}
        >
          <div className="bg-yellow-100 p-6 rounded-xl shadow-lg">
            <FaDollarSign className="text-4xl text-yellow-500 mb-4" />
            <h3 className="text-3xl font-semibold text-gray-800 mb-2">Give Budget & Preferences</h3>
            <p className="text-gray-600 text-2xl">
              Share your travel preferences and budget so we can personalize the recommendations.
            </p>
          </div>
        </motion.div>

        {/* Step 2 */}
        <motion.div
          className="flex flex-col items-center text-center"
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ type: "spring", stiffness: 100, damping: 25, delay: 0.4 }}
        >
          <div className="bg-yellow-100 p-6 rounded-xl shadow-lg">
            <FaLightbulb className="text-4xl text-yellow-500 mb-4" />
            <h3 className="text-3xl font-semibold text-gray-800 mb-2">Get Recommendations</h3>
            <p className="text-gray-600 text-2xl">
              Receive smart, AI-driven recommendations based on your preferences and budget.
            </p>
          </div>
        </motion.div>

        {/* Step 3 */}
        <motion.div
          className="flex flex-col items-center text-center"
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ type: "spring", stiffness: 100, damping: 25, delay: 0.6 }}
        >
          <div className="bg-yellow-100 p-6 rounded-xl shadow-lg">
            <FaMapMarkedAlt className="text-4xl text-yellow-500 mb-4" />
            <h3 className="text-3xl font-semibold text-gray-800 mb-2">Plan Trip</h3>
            <p className="text-gray-600 text-2xl">
              Effortlessly create and manage personalized travel itineraries — all in one place.
            </p>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

export default InteractionSequence;
