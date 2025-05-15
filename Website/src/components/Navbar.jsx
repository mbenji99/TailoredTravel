import logo from "../assets/logo.png";

function Navbar({ onNavigate }) {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
    onNavigate("home");
  };

  const scrollToWelcome = () => {
    const welcomeSection = document.getElementById("welcome");
    if (welcomeSection) {
      welcomeSection.scrollIntoView({ behavior: "smooth" });
    }
    onNavigate("home");
  };

  return (
    <nav className="navbar-wrapper flex items-center justify-between px-6 py-4 bg-white shadow-md sticky top-0 z-50">
      {/* Logo Scrolls to Top */}
      <div
        className="flex items-center cursor-pointer"
        onClick={scrollToTop}
      >
        <img
          src={logo}
          alt="Tailored Travels Logo"
          className="w-[90px] h-[90px] mr-3"
        />
        <span className="text-4xl font-semibold text-yellow-500">
          Tailored Travels
        </span>
      </div>

      {/* Navigation Links */}
      <ul className="flex space-x-6">
        <li>
          <button
            onClick={scrollToWelcome}
            className="bg-white text-black font-bold text-lg py-2 px-4 rounded-lg hover:bg-yellow-400 hover:text-white hover:scale-110 transition-transform ease-in-out duration-300"
          >
            Home
          </button>
        </li>
        <li>
          <button
            onClick={() => onNavigate("features")}
            className="bg-white text-black font-bold text-lg py-2 px-4 rounded-lg hover:bg-yellow-400 hover:text-white hover:scale-110 transition-transform ease-in-out duration-300"
          >
            Features
          </button>
        </li>
        <li>
          <button
            onClick={() => onNavigate("about")}
            className="bg-white text-black font-bold text-lg py-2 px-4 rounded-lg hover:bg-yellow-400 hover:text-white hover:scale-110 transition-transform ease-in-out duration-300"
          >
            About
          </button>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
