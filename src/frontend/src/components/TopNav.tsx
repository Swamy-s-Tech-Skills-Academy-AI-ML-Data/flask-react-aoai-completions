import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBell, faCircleUser } from "@fortawesome/free-solid-svg-icons";

interface TopNavProps {
    appTitle?: string;
    userName?: string; // placeholder for future auth integration
    onNotificationsClick?: () => void;
}

const TopNav: React.FC<TopNavProps> = ({
    appTitle = "Azure OpenAI Chat",
    userName = "Guest",
    onNotificationsClick
}) => {
    const userInitial = userName.charAt(0).toUpperCase();
    return (
        <header className="h-14 bg-white/90 backdrop-blur border-b border-gray-200 px-4 flex items-center justify-between shadow-sm">
            <div className="flex items-center gap-3 select-none">
                <span className="text-lg font-semibold tracking-wide text-gray-800">{appTitle}</span>
                <span className="text-xs px-2 py-0.5 rounded bg-blue-50 text-blue-600 border border-blue-200">Single Turn</span>
            </div>
            <div className="flex items-center gap-5">
                <button
                    aria-label="Notifications"
                    onClick={onNotificationsClick}
                    className="relative text-gray-500 hover:text-gray-700 transition"
                >
                    <FontAwesomeIcon icon={faBell} size="lg" />
                    <span className="absolute -top-1 -right-1 bg-red-500 text-white text-[0.6rem] font-bold leading-none px-1.5 py-0.5 rounded-full">1</span>
                </button>
                <div className="hidden sm:flex items-center gap-2 text-gray-600">
                    <FontAwesomeIcon icon={faCircleUser} size="lg" />
                    <span className="text-sm font-medium">{userName}</span>
                </div>
                <div className="sm:hidden w-9 h-9 rounded-full bg-gradient-to-br from-sky-500 to-blue-600 text-white flex items-center justify-center font-semibold shadow-inner">
                    {userInitial}
                </div>
                <button className="text-xs font-medium text-gray-600 hover:text-gray-800 border border-gray-300 rounded px-2 py-1 shadow-sm hover:bg-gray-50 transition">Logout</button>
            </div>
        </header>
    );
};

export default TopNav;
