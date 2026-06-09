import React, { useContext, useEffect } from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { SunIcon, MoonIcon, Bars3Icon, HomeIcon, RectangleStackIcon } from '@heroicons/react/24/outline';
import { themeChange } from 'theme-change';
import { AuthContext } from '../context/AuthContext';

function Layout() {
  const { userId, logout } = useContext(AuthContext);
  const location = useLocation();

  useEffect(() => {
    themeChange(false);
  }, []);

  const pageTitle = location.pathname.includes('studio') ? 'Flashcard Studio' :
                    location.pathname.includes('study') ? 'Study Session' :
                    'Dashboard';

  return (
    <div className="drawer lg:drawer-open h-screen">
      <input id="left-sidebar-drawer" type="checkbox" className="drawer-toggle" />

      {/* Page Content */}
      <div className="drawer-content flex flex-col h-full bg-base-200">
        {/* Header/Navbar */}
        <div className="navbar sticky top-0 bg-base-100 z-10 shadow-md">
          <div className="flex-1">
            <label htmlFor="left-sidebar-drawer" className="btn btn-square btn-ghost lg:hidden">
              <Bars3Icon className="w-6 h-6" />
            </label>
            <h1 className="text-2xl font-semibold ml-2">{pageTitle}</h1>
          </div>

          <div className="flex-none gap-2">
            {/* Theme Toggle */}
            <label className="swap swap-rotate btn btn-ghost btn-circle">
              <input type="checkbox" data-toggle-theme="dark,light" data-act-class="ACTIVECLASS" />
              <SunIcon className="swap-on w-6 h-6" />
              <MoonIcon className="swap-off w-6 h-6" />
            </label>

            {userId ? (
              <div className="dropdown dropdown-end">
                <div tabIndex={0} role="button" className="badge badge-primary badge-outline gap-2 p-3 cursor-pointer">
                  User: <span className="font-mono text-xs font-bold">{userId.substring(0, 8)}...</span>
                </div>
                <ul tabIndex={0} className="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52 mt-4">
                  <li><a onClick={logout}>Logout</a></li>
                </ul>
              </div>
            ) : (
              <div className="badge badge-neutral">Not Logged In</div>
            )}
          </div>
        </div>

        {/* Main Content Area */}
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
          <div className="h-16"></div>
        </main>
      </div>

      {/* Left Sidebar */}
      <div className="drawer-side z-30">
        <label htmlFor="left-sidebar-drawer" className="drawer-overlay"></label>
        <ul className="menu p-4 w-80 bg-base-100 min-h-full text-base-content border-r border-base-200">
          <li className="mb-4 font-bold text-2xl px-4 text-primary flex flex-row items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="w-8 h-8 text-primary">
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
            </svg>
            DashWind SRS
          </li>

          <li>
            <Link to="/dashboard" className={location.pathname === '/dashboard' ? 'active bg-base-200 font-semibold' : ''}>
              <HomeIcon className="w-5 h-5" />
              Dashboard
            </Link>
          </li>
          <li>
            <Link to={userId ? `/studio/${userId}` : '/studio'} className={location.pathname.includes('/studio') ? 'active bg-base-200 font-semibold' : ''}>
              <RectangleStackIcon className="w-5 h-5" />
              Studio (Create Cards)
            </Link>
          </li>
        </ul>
      </div>
    </div>
  );
}

export default Layout;
