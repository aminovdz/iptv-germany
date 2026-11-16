import { defineCollection, z } from 'astro:content';

const guidesCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    author: z.string().default('Redaktion German IPTV'),
    image: z.string().default('/images/hero-bg.webp'),
    imageAlt: z.string().default('German IPTV Ratgeber & Streaming Guide'),
    tags: z.array(z.string()).default(['German IPTV', 'Streaming', 'Anleitung']),
    featured: z.boolean().default(false),
    readingTime: z.string().default('6 Min. Lesezeit'),
    category: z.string().default('Ratgeber & Vergleiche'),
    targetKeyword: z.string().optional()
  })
});

export const collections = {
  guides: guidesCollection
};
