import React from 'react';
import { Card, CardHeader, CardContent, Box } from '@mui/material';

const SkeletonBar = ({ w = '100%', h = 16, mb = 10 }) => (
  <div className="shimmer" style={{ width: w, height: h, marginBottom: mb, borderRadius: 6 }} />
);

const SkeletonLoader = () => {
  return (
    <Card className="panel panel-frosted">
      <CardHeader title="Technical Analysis" subheader="Confluence" className="panel-header" />
      <CardContent>
        {/* Ticker and price */}
        <SkeletonBar w="40%" h={20} />
        <SkeletonBar w="30%" h={24} mb={16} />

        {/* Signal row */}
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', mb: 2 }}>
          <SkeletonBar w="18%" h={36} mb={0} />
          <SkeletonBar w="20%" h={14} mb={0} />
        </Box>

        {/* Trend & score & toggle */}
        <Box sx={{ display: 'flex', gap: 3, flexWrap: 'wrap', mb: 2 }}>
          <SkeletonBar w="24%" h={18} mb={0} />
          <SkeletonBar w="24%" h={18} mb={0} />
          <SkeletonBar w="14%" h={34} mb={0} />
        </Box>

        {/* Breakdown grid */}
        <SkeletonBar w="30%" h={18} />
        <div className="breakdown-grid breakdown-3cols">
          {[...Array(6)].map((_, idx) => (
            <React.Fragment key={idx}>
              <SkeletonBar w="100%" h={16} />
              <SkeletonBar w="70px" h={26} />
              <SkeletonBar w="40px" h={16} />
            </React.Fragment>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default SkeletonLoader;
