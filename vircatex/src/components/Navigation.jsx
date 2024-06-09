import React from "react";
import { Link, useLocation } from "react-router-dom";

const Navigation = () => {
  const location = useLocation();
  const pathnames = location.pathname.split("/").filter((x) => x);

  return (
    <div>
      <nav>
        {pathnames.map((name, index) => {
          const routeTo = `/${pathnames.slice(0, index + 1).join("/")}`;
          const isLast = index === pathnames.length - 1;
          return (
            <span key={index}>
              <Link to={routeTo}>
                {name.charAt(0).toUpperCase() + name.slice(1)}
              </Link>
              {!isLast && " > "}
            </span>
          );
        })}
      </nav>
    </div>
  );
};

export default Navigation;