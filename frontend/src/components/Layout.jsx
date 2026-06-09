import React, { useContext, useEffect, useRef } from 'react';
import { Outlet, NavLink, useLocation } from 'react-router-dom';
import { SunIcon, MoonIcon, Bars3Icon, HomeIcon, RectangleStackIcon, BellIcon, XMarkIcon } from '@heroicons/react/24/outline';
import { themeChange } from 'theme-change';
import { AuthContext } from '../context/AuthContext';

function Layout() {
  const { userId, logout } = useContext(AuthContext);
  const location = useLocation();
  const mainContentRef = useRef(null);

  // Initialize theme
  useEffect(() => {
    themeChange(false);
  }, []);

  // Scroll to top on route change
  useEffect(() => {
    if (mainContentRef.current) {
      mainContentRef.current.scroll({ top: 0, behavior: "smooth" });
    }
  }, [location.pathname]);

  const pageTitle = location.pathname.includes('studio') ? 'Flashcard Studio' :
                    location.pathname.includes('study') ? 'Study Session' :
                    'Dashboard';

  const closeSidebar = () => {
    document.getElementById('left-sidebar-drawer').click();
  };

  return (
    <>
      <div className="drawer lg:drawer-open">
        <input id="left-sidebar-drawer" type="checkbox" className="drawer-toggle" />

        {/* Page Content */}
        <div className="drawer-content flex flex-col h-screen">

          {/* Header/Navbar */}
          <div className="navbar sticky top-0 bg-base-100 z-10 shadow-md">
            <div className="flex-1">
              <label htmlFor="left-sidebar-drawer" className="btn btn-primary drawer-button lg:hidden">
                <Bars3Icon className="h-5 inline-block w-5" />
              </label>
              <h1 className="text-2xl font-semibold ml-2">{pageTitle}</h1>
            </div>

            <div className="flex-none">
              {/* Theme Toggle */}
              <label className="swap">
                <input type="checkbox" data-toggle-theme="dark,light" data-act-class="ACTIVECLASS" />
                <SunIcon className="swap-on fill-current w-6 h-6" />
                <MoonIcon className="swap-off fill-current w-6 h-6" />
              </label>

              {/* Notification Icon */}
              <button className="btn btn-ghost ml-4 btn-circle">
                <div className="indicator">
                  <BellIcon className="h-6 w-6"/>
                </div>
              </button>

              {/* Profile Dropdown */}
              {userId ? (
                <div className="dropdown dropdown-end ml-4">
                  <label tabIndex={0} className="btn btn-ghost btn-circle avatar">
                    <div className="w-10 rounded-full bg-primary text-primary-content flex items-center justify-center font-bold">
                      {userId.substring(0, 2).toUpperCase()}
                    </div>
                  </label>
                  <ul tabIndex={0} className="menu menu-compact dropdown-content mt-3 p-2 shadow bg-base-100 rounded-box w-52">
                    <li className="justify-between">
                      <a className="font-semibold text-primary">ID: {userId.substring(0, 8)}...</a>
                    </li>
                    <div className="divider mt-0 mb-0"></div>
                    <li><a onClick={logout}>Logout</a></li>
                  </ul>
                </div>
              ) : (
                <div className="badge badge-neutral ml-4">Not Logged In</div>
              )}
            </div>
          </div>

          {/* Main Content Area */}
          <main className="flex-1 overflow-y-auto md:pt-4 pt-4 px-6 bg-base-200" ref={mainContentRef}>
            <Outlet />
            <div className="h-16"></div>
          </main>

        </div>

        {/* Left Sidebar */}
        <div className="drawer-side z-30">
          <label htmlFor="left-sidebar-drawer" className="drawer-overlay"></label>
          <ul className="menu pt-2 w-80 bg-base-100 min-h-full text-base-content">

            <button className="btn btn-ghost bg-base-300 btn-circle z-50 top-0 right-0 mt-4 mr-2 absolute lg:hidden" onClick={closeSidebar}>
              <XMarkIcon className="h-5 inline-block w-5"/>
            </button>

            <li className="mb-2 font-semibold text-xl">
              <NavLink to="/dashboard" className="hover:bg-transparent focus:bg-transparent active:bg-transparent">
                {/* Simulated Logo */}
                <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center text-primary-content">
                  <RectangleStackIcon className="w-6 h-6" />
                </div>
                DashWind
              </NavLink>
            </li>

            <li className="mt-4">
              <NavLink
                to="/dashboard"
                className={({isActive}) => `${isActive ? 'font-semibold bg-base-200' : 'font-normal'} relative`}
              >
                <HomeIcon className="w-5 h-5" /> Dashboard
                {location.pathname === '/dashboard' && (
                  <span className="absolute inset-y-0 left-0 w-1 rounded-tr-md rounded-br-md bg-primary" aria-hidden="true"></span>
                )}
              </NavLink>
            </li>

            <li>
              <NavLink
                to={userId ? `/studio/${userId}` : '/studio'}
                className={({isActive}) => `${isActive ? 'font-semibold bg-base-200' : 'font-normal'} relative`}
              >
                <RectangleStackIcon className="w-5 h-5" /> Flashcard Studio
                {location.pathname.includes('/studio') && (
                  <span className="absolute inset-y-0 left-0 w-1 rounded-tr-md rounded-br-md bg-primary" aria-hidden="true"></span>
                )}
              </NavLink>
            </li>

          </ul>
        </div>
      </div>
    </>
  );
}

export default Layout;
