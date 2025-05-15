import React, { useState } from "react";
import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import Welcome from "./components/Welcome";
import Features from "./components/Features";
import About from "./components/About";
import Footer from "./components/Footer";
import "./App.css";

function App() {
  const [currentSection, setCurrentSection] = useState("home");

  const renderSection = () => {
    switch (currentSection) {
      case "features":
        return <Features />;
      case "about":
        return <About />;
      case "home":
      default:
        return <Welcome />;
    }
  };

  return (
    <>
      <Navbar onNavigate={setCurrentSection} />
      <Hero showContent={currentSection === "home"} />
      {renderSection()}
      <Footer />
    </>
  );
}

export default App;
