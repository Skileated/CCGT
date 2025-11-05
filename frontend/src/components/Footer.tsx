import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer className="bg-gray-50 text-center text-sm text-gray-600 py-8">
      <div className="space-x-4 mb-2">
        <Link to="/" className="hover:text-indigo-600 transition">Home</Link>
        <span>|</span>
        <Link to="/demo" className="hover:text-indigo-600 transition">Try Demo</Link>
        <span>|</span>
        <a href="#contact" className="hover:text-indigo-600 transition">Contact</a>
        <span>|</span>
        <a href="https://github.com/Skileated/CCGT" target="_blank" rel="noopener noreferrer" className="hover:text-indigo-600 transition">GitHub</a>
      </div>
      <div>© 2025 CCGT Project Team. All rights reserved.</div>
    </footer>
  );
}

