const primary =  '#3366EF';
const success =  '#82D31F';
const info =  '#42B6FF';
const warning =  '#FFD905';
const danger =  '#FF7226';

export const LIGHT_THEME = {
  name: 'light',
  base: 'default',
  variables: {
    primary,
    success,
    info,
    warning,
    danger,
    charts: {
      primary,
      success,
      info,
      warning,
      danger,
      bg: 'transparent',
      textColor: '#1A2138',
      axisLineColor: '#8F9BB3',
      splitLineColor: '#C5CEE0',
      itemHoverShadowColor: 'rgba(0, 0, 0, 0.5)',
      tooltipBackgroundColor: '#E4E9F2',
      areaOpacity: '0.7',
    },
    bubbleMap: {
      primary,
      success,
      info,
      warning,
      danger,
      titleColor: '#1A2138',
      areaColor: '#EDF1F7',
      areaHoverColor: '#E4E9F2',
      areaBorderColor: '#F7F9FC',
    },
  },
};
