
import logo from "../assets/logo.png";

function Logo({ size = "h-10" }) {
  return (
    <div className="flex items-center space-x-2">
      <img src={logo} alt="Tailored Travels" className={`${size} w-auto`} />
      <span className="text-white font-bold text-xl">Tailored Travels</span>
    </div>
  );
}

export default Logo;
