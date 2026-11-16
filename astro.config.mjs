import { defineConfig } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://germaniptv.cloud',
  output: 'static',
  trailingSlash: 'always',
  adapter: cloudflare({
    imageService: 'compile'
  }),
  integrations: [
    sitemap({
      filter: (page) => !page.includes('/404') && !page.includes('/admin') && !page.includes('/iptv-germany'),
      changefreq: 'daily',
      priority: 0.9,
      lastmod: new Date()
    })
  ],
  vite: {
    plugins: [tailwindcss()]
  },
  build: {
    inlineStylesheets: 'auto'
  }
});
