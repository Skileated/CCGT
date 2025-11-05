import { useLocation, useNavigate } from 'react-router-dom';

export default function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();

  const isActive = (path: string) => {
    if (path === '/' && location.pathname === '/') return true;
    return location.pathname.startsWith(path);
  };

  const goHome = (e: React.MouseEvent) => {
    e.preventDefault();
    if (location.pathname !== '/') navigate('/');
    else {
      const el = document.getElementById('home');
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  const goDemo = (e: React.MouseEvent) => {
    e.preventDefault();
    navigate('/demo');
  };

  const goContact = (e: React.MouseEvent) => {
    e.preventDefault();
    if (location.pathname !== '/') {
      navigate('/');
      setTimeout(() => {
        const el = document.getElementById('contact');
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
    } else {
      const el = document.getElementById('contact');
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <nav className="flex justify-between items-center px-8 py-4 shadow-sm bg-white fixed top-0 w-full z-50">
      <div onClick={() => navigate('/')} className="text-2xl font-bold text-indigo-600 cursor-pointer">CCGT</div>
      <div className="flex space-x-8 text-gray-700 font-medium">
        <a href="#home" onClick={goHome} className={`hover:text-indigo-600 transition ${isActive('/') ? 'text-indigo-600' : ''}`}>Home</a>
        <a href="/demo" onClick={goDemo} className={`hover:text-indigo-600 transition ${isActive('/demo') ? 'text-indigo-600' : ''}`}>Try Demo</a>
        <a href="#contact" onClick={goContact} className="hover:text-indigo-600 transition">Contact Us</a>
        <a href="https://github.com/Skileated/CCGT" target="_blank" rel="noopener noreferrer" className="text-gray-700 hover:text-indigo-600 transition" aria-label="GitHub">
          <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 .5C5.65.5.5 5.65.5 12c0 5.1 3.29 9.43 7.86 10.96.57.1.78-.25.78-.56v-2c-3.2.7-3.87-1.38-3.87-1.38-.52-1.33-1.26-1.68-1.26-1.68-1.03-.7.08-.68.08-.68 1.15.08 1.75 1.18 1.75 1.18 1 .1 2.24 1.68 2.24 1.68.9 1.54 2.64 1.1 3.28.84.1-.67.35-1.1.63-1.35-2.55-.28-5.23-1.26-5.23-5.6 0-1.24.43-2.25 1.14-3.05-.12-.28-.49-1.44.1-3 0 0 .96-.31 3.15 1.18a10.9 10.9 0 0 1 5.74 0C17.4 7.57 18.4 7.88 18.4 7.88c.59 1.56.22 2.72.1 3 .71.8 1.14 1.81 1.14 3.05 0 4.35-2.68 5.32-5.24 5.6.36.3.68.92.68 1.86v2.76c0 .3.21.66.79.55C20.21 21.43 23.5 17.1 23.5 12 23.5 5.65 18.35.5 12 .5z"/>
          </svg>
        </a>
      </div>
    </nav>
  );
}


