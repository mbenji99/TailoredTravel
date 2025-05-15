import React from 'react';
import { motion } from 'framer-motion';
import backgroundImage from '../assets/fbg-image.jpg';

const featureVariants = {
  hidden: { opacity: 0, y: 50 },
  visible: (i) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.2, duration: 0.6, ease: 'easeOut' }
  })
};

function Features() {
  return (
    <motion.section
      id="features"
      className="relative w-full min-h-[75vh] bg-fixed bg-cover bg-center px-6 py-20 flex flex-col items-center justify-center"
      style={{ backgroundImage: `url(${backgroundImage})`, transform: 'translateZ(0)' }}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, amount: 0.3 }}
    >
      <motion.h2
        className="text-5xl font-bold text-center text-white-100 mb-12"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        Explore What Tailored Travels Offers
      </motion.h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-10 max-w-6xl w-full">
        {[
          {
            title: 'AI-Powered Personalization',
            desc: `We understand your preferences through simple inputs and feedback. From quiet mountain retreats to vibrant city adventures, our AI engine recommends places, stays, and experiences made just for you.`
          },
          {
            title: 'Budget-Conscious Smart Planning',
            desc: `Give us your travel budget — we’ll give you the best trip for your money. Our system dynamically adjusts suggestions in real time using real-world price data, ensuring both quality and value.`
          },
          {
            title: 'Build Flexible Itineraries',
            desc: `Tailored Travels helps you design without committing. Explore multiple smart itinerary options, swap elements with ease, and export your plan. We don’t book trips — we help you build better ones.`
          }
        ].map((feature, i) => (
          <motion.div
            key={feature.title}
            className="p-6 bg-white/90 shadow-md rounded-lg cursor-pointer hover:shadow-xl backdrop-blur-sm"
            custom={i}
            variants={featureVariants}
            whileHover={{ scale: 1.05 }}
            transition={{ type: 'spring', stiffness: 300 }}
          >
            <h3 className="font-bold text-3xl mb-3 text-red-800">{feature.title}</h3>
            <p className="text-black-500 text-3xl font-bold text-base leading-relaxed">{feature.desc}</p>
          </motion.div>
        ))}
      </div>
    </motion.section>
  );
}

export default Features;
