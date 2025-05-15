import React from "react";
import { FaTwitter, FaFacebookF, FaInstagram, FaEnvelope, FaPhone } from "react-icons/fa";

function Footer() {
  return (
    <footer className="bg-yellow-500 text-black py-6 px-4 text-center md:text-left">
      <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
        
        {/* Contact Info */}
        <div className="space-y-2">
          <h4 className="text-base text-s font-bold">Contact Us</h4>
          <p className="flex items-center gap-2 text-s text-gray-800">
            <FaEnvelope /> support@tailoredtravels.com
          </p>
          <p className="flex items-center gap-2 text-s text-gray-800">
            <FaPhone /> +1 (800) 555-1234
          </p>
        </div>

        {/* Social Media */}
        <div className="flex justify-center space-x-5">
          <a href="https://twitter.com" target="_blank" rel="noopener noreferrer">
            <FaTwitter className="text-2xl hover:text-yellow-300" />
          </a>
          <a href="https://facebook.com" target="_blank" rel="noopener noreferrer">
            <FaFacebookF className="text-2xl hover:text-yellow-300" />
          </a>
          <a href="https://instagram.com" target="_blank" rel="noopener noreferrer">
            <FaInstagram className="text-2xl hover:text-yellow-300" />
          </a>
        </div>

        {/* Quick Action / CTA */}
        <div className="flex flex-col items-center md:items-end space-y-2">
          <h4 className="text-base font-bold">Need Help?</h4>
          <a
            href="mailto:support@tailoredtravels.com"
            className="inline-block bg-black text-white px-4 py-1.5 rounded-md text-sm hover:bg-gray-800 transition-all"
          >
            Email Us
          </a>
        </div>
      </div>

      {/* Bottom Copyright */}
      <div className="mt-6 text-s text-gray-700 text-center border-t pt-3 border-black/30">
        © 2025 Tailored Travels. All Rights Reserved.
      </div>
    </footer>
  );
}

export default Footer;
