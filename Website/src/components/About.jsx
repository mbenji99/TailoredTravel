import { motion } from "framer-motion";
import { FaMapMarkedAlt, FaSmileBeam, FaRobot } from "react-icons/fa";
import aboutBackground from "../assets/about-bg.png";

function About() {
  return (
    <section
      id="about"
      className="relative w-full min-h-screen bg-fixed bg-cover bg-[position:50%_74%] px-6 pt-10 pb-20 flex items-start justify-center"
      style={{ backgroundImage: `url(${aboutBackground})`, transform: "translateZ(0)" }}
    >
      <motion.div
        className="bg-white/90 backdrop-blur-md p-20 pt-25 rounded-2xl max-w-6xl shadow-2xl grid grid-cols-1 md:grid-cols-2 gap-16 -mt-16"
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ type: "spring", stiffness: 100, damping: 20 }}
        viewport={{ once: true, amount: 0.3 }}
      >
        {/* Left column – Text content */}
        <div className="text-left space-y-8">
          <h2 className="text-5xl font-semibold text-yellow-500">
            Why Tailored Travels?
          </h2>
          <ul className="space-y-6 text-gray-700 text-lg">
            <li className="flex items-start gap-4">
              <FaMapMarkedAlt className="text-yellow-500 text-5xl mt-1" />
              <span className="font-medium text-xl">
                <strong>Clarity over chaos:</strong> Say goodbye to decision overload with smart, minimal choices.
              </span>
            </li>
            <li className="flex items-start gap-4">
              <FaRobot className="text-yellow-500 text-6xl mt-1" />
              <span className="font-medium text-xl">
                <strong>AI that gets you:</strong> Your vibe, your budget, your pace — our engine personalizes every step.
              </span>
            </li>
            <li className="flex items-start gap-4">
              <FaSmileBeam className="text-yellow-500 text-4xl mt-1" />
              <span className="font-medium text-xl">
                <strong>Built for joy:</strong> Travel planning should feel fun, not frustrating.
              </span>
            </li>
          </ul>
        </div>

        {/* Right column – Summary statement */}
        <div className="text-center md:text-left flex flex-col justify-center space-y-6">
          <blockquote className="text-3xl italic text-gray-800 font-semibold border-l-4 border-yellow-400 pl-6">
            "Tailored Travels isn’t just a platform — it's your AI co-pilot for adventures."
          </blockquote>
          <p className="text-xl text-gray-600  font-semibold">
            Built for modern explorers who value relevance, simplicity, and a touch of delight.
          </p>
        </div>
      </motion.div>
    </section>
  );
}

export default About;
