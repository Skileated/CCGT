import { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import Footer from '../components/Footer';
import { submitContact } from '../api';

export default function Home() {
  const navigate = useNavigate();
  const [contactOk, setContactOk] = useState<string | null>(null);
  const formRef = useRef<HTMLFormElement>(null);

  const handleDemoClick = () => {
    navigate('/demo');
  };

  const handleCTAClick = () => {
    const el = document.getElementById('contact');
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  const heroVariants = {
    hidden: { opacity: 0, y: 40 },
    visible: { opacity: 1, y: 0, transition: { duration: 1 } },
  };

  return (
    <div>
      {/* Hero Section */}
      <section id="home" className="min-h-[80vh] flex flex-col items-center justify-center text-center bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white px-6 relative overflow-hidden">
        {/* Subtle floating nodes background */}
        <div className="absolute inset-0 opacity-20 pointer-events-none">
          <svg className="w-full h-full" preserveAspectRatio="none">
            <defs>
              <radialGradient id="g" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stopColor="#ffffff" />
                <stop offset="100%" stopColor="transparent" />
              </radialGradient>
            </defs>
            <circle cx="20%" cy="30%" r="120" fill="url(#g)"></circle>
            <circle cx="80%" cy="40%" r="160" fill="url(#g)"></circle>
            <circle cx="50%" cy="80%" r="140" fill="url(#g)"></circle>
          </svg>
        </div>
        <motion.div
          initial="hidden"
          animate="visible"
          variants={heroVariants}
          className="max-w-3xl"
        >
          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1 }}
            className="text-5xl font-bold mb-4"
          >
            What is CCGT?
          </motion.h1>
          <motion.p className="text-lg sm:text-xl opacity-90 mb-8" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.4 }}>
            The Contextual Coherence Graph Transformer (CCGT) evaluates how well sentences connect within a paragraph.
          </motion.p>
          <div className="flex items-center justify-center gap-3">
            <button onClick={handleDemoClick} className="px-6 py-3 rounded-xl bg-white/10 hover:bg-white/20 transition-all duration-300 shadow-lg border border-white/20">
              Try Live Demo
            </button>
            <button onClick={handleCTAClick} className="px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-700 transition-all duration-300 shadow-lg">
              Contact Us
            </button>
          </div>
        </motion.div>
      </section>
      {/* Core Features Grid */}
      <section className="max-w-6xl mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Core Features</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {[
            { title: 'Semantic Graph Builder', desc: 'Builds sentence graphs using similarity + discourse.' },
            { title: 'Entropy Analyzer', desc: 'Quantifies structural coherence.' },
            { title: 'Graph Transformer Encoder', desc: 'Learns multi-hop contextual relations.' },
            { title: 'Coherence Scoring Engine', desc: 'Generates interpretable coherence score (0–1).' },
            { title: 'Disruption Report', desc: 'Detects incoherent transitions.' },
            { title: 'REST API + Dashboard', desc: 'Integrate easily via FastAPI or Web UI.' }
          ].map((f, idx) => (
            <motion.div key={f.title} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: idx * 0.05 }}
              className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-shadow">
              <div className="text-lg font-semibold mb-2 text-gray-800">{f.title}</div>
              <div className="text-gray-600">{f.desc}</div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Target Users */}
      <section className="max-w-6xl mx-auto px-4 py-16 grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Who is it for?</h2>
          <p className="text-gray-600">CCGT serves teams who care about coherent, readable, logically connected writing.</p>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {[
            'AI Researchers — Evaluate LLM consistency',
            'EdTech — Essay feedback',
            'Writers — Transition quality',
            'Enterprise — Secure on-premise deployment',
          ].map((t) => (
            <div key={t} className="bg-white rounded-xl shadow p-4 text-gray-800">{t}</div>
          ))}
        </div>
      </section>

      {/* Architecture Snapshot */}
      <section className="max-w-6xl mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">How it works</h2>
        <div className="bg-white rounded-2xl shadow-lg p-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 text-gray-800">
            {[
              'Input Text', 'Sentence-BERT', 'Graph Builder', 'Entropy Analyzer', 'Graph Transformer', 'Coherence Score + Report'
            ].map((step, i) => (
              <>
                <motion.div key={step} initial={{ opacity: 0, y: 10 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="font-medium">
                  {step}
                </motion.div>
                {i < 5 && <div className="hidden md:block text-gray-400">→</div>}
              </>
            ))}
          </div>
        </div>
      </section>

      {/* API & Deployment */}
      <section className="max-w-6xl mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">API & Deployment</h2>
        <div className="bg-white rounded-2xl shadow p-6 text-gray-800 space-y-4">
          <div>
            <div className="font-semibold mb-2">Endpoints:</div>
            <ul className="list-disc ml-6">
              <li>POST /analyze → score, report, visualization</li>
              <li>GET /health → system status</li>
            </ul>
          </div>
          <div>
            <div className="font-semibold mb-2">Deployment:</div>
            <div>☁️ Docker REST API | 💻 CLI | 🌐 Web Dashboard</div>
          </div>
        </div>
      </section>

      {/* Performance & Security */}
      <section className="max-w-6xl mx-auto px-4 py-16 grid grid-cols-1 sm:grid-cols-3 gap-4">
        {[
          'Fast — ≤ 2s per 500 words',
          'Secure — JWT/OAuth ready',
          'Portable — Works on AWS, Azure, On-Prem'
        ].map((b) => (
          <div key={b} className="bg-white rounded-xl shadow p-6 text-center text-gray-800">{b}</div>
        ))}
      </section>

      {/* CTA Section */}
      <section className="text-center px-4 py-16">
        <h2 className="text-2xl sm:text-3xl font-bold mb-6 text-gray-800">Experience coherence analysis like never before.</h2>
        <div className="flex flex-wrap items-center justify-center gap-3">
          <button onClick={handleDemoClick} className="px-6 py-3 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white transition-all">Try Live Demo</button>
          <a href="https://github.com/Skileated/CCGT" target="_blank" rel="noopener noreferrer" className="px-6 py-3 rounded-lg bg-white border border-gray-200 text-gray-800 hover:bg-gray-50 transition-all">View on GitHub</a>
          <a href="#" className="px-6 py-3 rounded-lg bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white hover:opacity-90 transition-all">Download Whitepaper</a>
        </div>
      </section>

      {/* Contact Us Section */}
      <section id="contact" className="max-w-xl mx-auto px-4 py-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="bg-white rounded-2xl shadow-lg p-8"
        >
          <h2 className="text-2xl font-semibold mb-4 text-center text-gray-800">Contact Us</h2>
          <form
            ref={formRef}
            onSubmit={async (e) => {
              e.preventDefault();
              setContactOk(null);
              
              // Get form element reference - use ref if available, otherwise use currentTarget
              const form = formRef.current || (e.currentTarget as HTMLFormElement);
              if (!form) {
                console.error('Form element not found');
                return;
              }
              
              const formData = new FormData(form);
              const name = formData.get('name') as string;
              const email = formData.get('email') as string;
              const organization = formData.get('organization') as string;
              const message = formData.get('message') as string;
              
              try {
                const data = await submitContact({ name, email, organization, message });
                // If we get here, the request was successful (no exception thrown)
                // The CSV is being updated, so show success message
                setContactOk('Thank you! We\'ll reach out soon.');
                
                // Reset form safely
                if (form) {
                  form.reset();
                }
              } catch (err: any) {
                console.error('Form submission error:', err);
                
                // Extract error message from various error formats
                let errorMessage = 'Error submitting form. Please try again.';
                
                if (err.message) {
                  errorMessage = err.message;
                } else if (err.response?.data?.detail) {
                  errorMessage = err.response.data.detail;
                } else if (err.response?.data?.message) {
                  errorMessage = err.response.data.message;
                } else if (typeof err === 'string') {
                  errorMessage = err;
                }
                
                setContactOk(`Error: ${errorMessage}`);
              }
            }}
            className="space-y-4"
          >
            <input name="name" placeholder="Name" className="w-full border border-gray-300 rounded-lg p-3 focus:outline-none focus:border-indigo-500" required />
            <input name="email" type="email" placeholder="Email" className="w-full border border-gray-300 rounded-lg p-3 focus:outline-none focus:border-indigo-500" required />
            <input name="organization" placeholder="Organization" className="w-full border border-gray-300 rounded-lg p-3 focus:outline-none focus:border-indigo-500" required />
            <textarea name="message" placeholder="Message" className="w-full border border-gray-300 rounded-lg p-3 h-24 focus:outline-none focus:border-indigo-500" required></textarea>
            <button type="submit" className="w-full bg-indigo-600 text-white py-3 rounded-lg hover:bg-indigo-700 transition-all">Submit</button>
            {contactOk && (
              <div className={`text-center ${contactOk.startsWith('Error') ? 'text-red-600' : 'text-green-600'}`}>
                {contactOk}
              </div>
            )}
          </form>
        </motion.div>
      </section>

      <Footer />
    </div>
  );
}

