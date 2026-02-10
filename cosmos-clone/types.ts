export interface NavItem {
  label: string;
  href: string;
}

export interface ImageCard {
  id: string;
  src: string;
  alt: string;
  width?: number; // Optional distinct width for masonry effect
  aspectRatio?: string;
  title?: string;
  author?: string;
}

export interface FeatureProps {
  title: string;
  description: string;
  image: string;
  reverse?: boolean;
}